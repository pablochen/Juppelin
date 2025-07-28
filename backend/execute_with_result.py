import sys
import os
import json
import traceback
import pandas as pd
from io import StringIO

# shared 폴더의 user_functions 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir = os.path.join(current_dir, '..', 'shared')
sys.path.insert(0, shared_dir)

global_ns = {}
local_ns = {}

try:
    from user_functions import *
    
    # 전역 네임스페이스에 모든 user_functions 추가
    import user_functions
    for name in dir(user_functions):
        if not name.startswith('_'):
            obj = getattr(user_functions, name)
            if callable(obj):
                global_ns[name] = obj
                local_ns[name] = obj
    
    # pandas, numpy도 기본으로 추가
    import pandas as pd
    import numpy as np
    global_ns['pd'] = pd
    global_ns['np'] = np
    local_ns['pd'] = pd
    local_ns['np'] = np
    
except Exception as e:
    # Silently fail user functions import
    pass

code = sys.argv[1]

# DataFrame 결과를 잡기 위한 헬퍼
class DFResultCatcher:
    def __init__(self):
        self.df_result = None
        self.df_type = None
    def set(self, obj):
        if isinstance(obj, pd.DataFrame):
            self.df_result = obj
            self.df_type = 'dataframe'
        elif hasattr(obj, 'to_dict'):
            self.df_result = obj
            self.df_type = 'series'
        else:
            self.df_result = None
            self.df_type = None

catcher = DFResultCatcher()

# 마지막 줄 결과를 잡기 위한 코드 래핑
user_code = code.strip()

# DataFrame 할당 감지를 위한 변수
last_df_assignment = None

if '\n' in user_code:
    lines = user_code.split('\n')
    last = lines[-1].strip()
    
    # 전체 코드 실행
    exec('\n'.join(lines[:-1]), global_ns, local_ns)
    
    # 마지막 줄이 변수명만 있는 경우 (예: "data")
    if last and not ('=' in last or '(' in last or '[' in last):
        # 단순 변수 출력인 경우에만 DataFrame 체크
        try:
            result = eval(last, global_ns, local_ns)
            if isinstance(result, (pd.DataFrame, pd.Series)):
                catcher.set(result)
            else:
                # DataFrame이 아닌 경우 일반 실행
                exec(last, global_ns, local_ns)
        except Exception:
            exec(last, global_ns, local_ns)
    else:
        # 복잡한 표현식인 경우 일반 실행
        try:
            result = eval(last, global_ns, local_ns)
            # DataFrame 할당이 아닌 경우에만 출력 체크
            if '=' not in last:
                catcher.set(result)
        except Exception:
            exec(last, global_ns, local_ns)
else:
    # 한 줄 코드인 경우
    # 할당문인지 확인
    if '=' in user_code and not ('==' in user_code or '!=' in user_code or '<=' in user_code or '>=' in user_code):
        # 할당문이면 실행만 하고 DataFrame 추출 안함
        exec(user_code, global_ns, local_ns)
    else:
        # 일반 표현식이면 결과 확인
        try:
            result = eval(user_code, global_ns, local_ns)
            catcher.set(result)
        except Exception:
            exec(user_code, global_ns, local_ns)
        exec(user_code, global_ns, local_ns)

# DataFrame/Series 결과가 있으면 JSON으로 출력
if catcher.df_type == 'dataframe':
    # DataFrame을 JSON 직렬화 가능하도록 변환
    df_copy = catcher.df_result.head(100).copy()
    
    # 날짜/시간 컬럼을 문자열로 변환
    for col in df_copy.columns:
        if df_copy[col].dtype.name.startswith('datetime') or 'timestamp' in str(df_copy[col].dtype).lower():
            df_copy[col] = df_copy[col].astype(str)
    
    # 인덱스 처리 - 항상 문자열로 변환하고 이름 포함
    index_name = df_copy.index.name or 'Index'
    index_list = []
    for idx in df_copy.index:
        if hasattr(idx, 'strftime'):  # datetime-like
            index_list.append(str(idx))
        else:
            index_list.append(str(idx))
    
    # to_dict 변환 시 JSON 직렬화 가능한 형태로
    data_dict = df_copy.to_dict(orient='split')
    
    # 데이터 내의 모든 값을 JSON 직렬화 가능하도록 변환
    clean_data = []
    for row in data_dict['data']:
        clean_row = []
        for val in row:
            if pd.isna(val):
                clean_row.append(None)
            elif hasattr(val, 'strftime'):  # datetime-like
                clean_row.append(str(val))
            elif hasattr(val, 'item'):  # numpy scalar
                try:
                    clean_row.append(val.item())
                except:
                    clean_row.append(str(val))
            else:
                clean_row.append(val)
        clean_data.append(clean_row)
    
    print("__DF_JSON_START__" + json.dumps({
        'type': 'dataframe',
        'columns': list(df_copy.columns),
        'index_name': index_name,
        'data': {
            'columns': data_dict['columns'],
            'index': index_list,
            'data': clean_data
        }
    }) + "__DF_JSON_END__")
elif catcher.df_type == 'series':
    # Series도 동일하게 처리
    series_copy = catcher.df_result.head(100).copy()
    if series_copy.dtype.name.startswith('datetime') or 'timestamp' in str(series_copy.dtype).lower():
        series_copy = series_copy.astype(str)
    
    # 인덱스 이름 포함
    index_name = series_copy.index.name or 'Index'
    clean_dict = {}
    for k, v in series_copy.to_dict().items():
        if pd.isna(v):
            clean_dict[str(k)] = None
        elif hasattr(v, 'strftime'):
            clean_dict[str(k)] = str(v)
        elif hasattr(v, 'item'):
            clean_dict[str(k)] = v.item()
        else:
            clean_dict[str(k)] = v
    
    print("__DF_JSON_START__" + json.dumps({
        'type': 'series',
        'index_name': index_name,
        'data': clean_dict
    }) + "__DF_JSON_END__")
