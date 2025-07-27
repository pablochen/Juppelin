"""
Visualization Service
Plotly 기반 차트 생성 서비스
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class VisualizationService:
    """시각화 서비스"""
    
    def __init__(self):
        # 다크 테마 설정
        self.theme = 'plotly_dark'
        self.color_palette = {
            'primary': '#61DAFB',
            'secondary': '#FF6B6B', 
            'tertiary': '#4ECDC4',
            'background': '#1E1E1E',
            'grid': '#333333',
            'text': '#A9B7C6'
        }
    
    def create_candlestick_chart(
        self,
        data: pd.DataFrame,
        title: str = "캔들스틱 차트",
        height: int = 600,
        show_volume: bool = True
    ) -> Dict[str, Any]:
        """
        캔들스틱 차트 생성
        
        Args:
            data: OHLCV 데이터
            title: 차트 제목
            height: 차트 높이
            show_volume: 거래량 표시 여부
        
        Returns:
            Plotly 차트 JSON 데이터
        """
        try:
            # 서브플롯 생성 (거래량 포함 시 2개, 아니면 1개)
            if show_volume:
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.03,
                    subplot_titles=[title, '거래량'],
                    row_width=[0.7, 0.3]
                )
            else:
                fig = go.Figure()
            
            # 캔들스틱 차트 추가
            candlestick = go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name='가격',
                increasing_line_color=self.color_palette['primary'],
                decreasing_line_color=self.color_palette['secondary']
            )
            
            if show_volume:
                fig.add_trace(candlestick, row=1, col=1)
                
                # 거래량 바 차트 추가
                colors = ['red' if close < open else 'green' 
                         for close, open in zip(data['close'], data['open'])]
                
                volume_bar = go.Bar(
                    x=data.index,
                    y=data['volume'],
                    name='거래량',
                    marker_color=colors,
                    showlegend=False
                )
                fig.add_trace(volume_bar, row=2, col=1)
            else:
                fig.add_trace(candlestick)
                fig.update_layout(title=title)
            
            # 레이아웃 설정
            fig.update_layout(
                template=self.theme,
                height=height,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            # x축 설정
            fig.update_xaxes(
                type='date',
                showgrid=True,
                gridcolor=self.color_palette['grid']
            )
            
            # y축 설정
            fig.update_yaxes(
                showgrid=True,
                gridcolor=self.color_palette['grid']
            )
            
            logger.info(f"캔들스틱 차트 생성 완료: {len(data)}개 캔들")
            return json.loads(fig.to_json())
            
        except Exception as e:
            logger.error(f"캔들스틱 차트 생성 실패: {e}")
            raise
    
    def create_line_chart(
        self,
        data: pd.DataFrame,
        columns: List[str],
        title: str = "선 그래프",
        height: int = 400
    ) -> Dict[str, Any]:
        """
        선 그래프 생성
        
        Args:
            data: 데이터
            columns: 표시할 컬럼 리스트
            title: 차트 제목
            height: 차트 높이
        
        Returns:
            Plotly 차트 JSON 데이터
        """
        try:
            fig = go.Figure()
            
            colors = [self.color_palette['primary'], self.color_palette['secondary'], 
                     self.color_palette['tertiary']] * 10  # 색상 반복
            
            for i, column in enumerate(columns):
                if column in data.columns:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data[column],
                        mode='lines',
                        name=column,
                        line=dict(color=colors[i % len(colors)], width=2)
                    ))
            
            # 레이아웃 설정
            fig.update_layout(
                title=title,
                template=self.theme,
                height=height,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            # 축 설정
            fig.update_xaxes(
                showgrid=True,
                gridcolor=self.color_palette['grid']
            )
            fig.update_yaxes(
                showgrid=True,
                gridcolor=self.color_palette['grid']
            )
            
            logger.info(f"선 그래프 생성 완료: {len(columns)}개 라인")
            return json.loads(fig.to_json())
            
        except Exception as e:
            logger.error(f"선 그래프 생성 실패: {e}")
            raise
    
    def create_technical_analysis_chart(
        self,
        data: pd.DataFrame,
        indicators: Dict[str, pd.DataFrame],
        title: str = "기술적 분석",
        height: int = 800
    ) -> Dict[str, Any]:
        """
        기술적 분석 복합 차트 생성
        
        Args:
            data: OHLCV 데이터
            indicators: 기술 지표 데이터 딕셔너리
            title: 차트 제목
            height: 차트 높이
        
        Returns:
            Plotly 차트 JSON 데이터
        """
        try:
            # 서브플롯 개수 계산 (가격 + 지표별)
            num_subplots = 1 + len(indicators)
            
            fig = make_subplots(
                rows=num_subplots, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.02,
                subplot_titles=[title] + list(indicators.keys()),
                row_heights=[0.5] + [0.5/(num_subplots-1)]*(num_subplots-1) if num_subplots > 1 else [1.0]
            )
            
            # 1. 캔들스틱 차트
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'], 
                    low=data['low'],
                    close=data['close'],
                    name='가격',
                    increasing_line_color=self.color_palette['primary'],
                    decreasing_line_color=self.color_palette['secondary']
                ),
                row=1, col=1
            )
            
            # 2. 기술 지표들
            colors = [self.color_palette['primary'], self.color_palette['secondary'], 
                     self.color_palette['tertiary']]
            
            for i, (indicator_name, indicator_data) in enumerate(indicators.items()):
                row_num = i + 2
                
                # 각 지표의 컬럼들을 개별 라인으로 추가
                for j, column in enumerate(indicator_data.columns):
                    fig.add_trace(
                        go.Scatter(
                            x=indicator_data.index,
                            y=indicator_data[column],
                            mode='lines',
                            name=f"{indicator_name}_{column}",
                            line=dict(color=colors[j % len(colors)], width=2),
                            showlegend=True
                        ),
                        row=row_num, col=1
                    )
                
                # 특별한 기준선 추가 (RSI의 경우)
                if 'rsi' in indicator_name.lower():
                    # RSI 70, 30 기준선
                    for level, color in [(70, 'red'), (30, 'green')]:
                        fig.add_hline(
                            y=level, line_dash="dash", line_color=color,
                            row=row_num, col=1
                        )
            
            # 레이아웃 설정
            fig.update_layout(
                template=self.theme,
                height=height,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            # 모든 x축 설정
            fig.update_xaxes(
                type='date',
                showgrid=True,
                gridcolor=self.color_palette['grid']
            )
            
            # 모든 y축 설정
            fig.update_yaxes(
                showgrid=True,
                gridcolor=self.color_palette['grid']
            )
            
            logger.info(f"기술적 분석 차트 생성 완료: {len(indicators)}개 지표")
            return json.loads(fig.to_json())
            
        except Exception as e:
            logger.error(f"기술적 분석 차트 생성 실패: {e}")
            raise
    
    def create_correlation_heatmap(
        self,
        data: pd.DataFrame,
        title: str = "상관관계 히트맵",
        height: int = 500
    ) -> Dict[str, Any]:
        """
        상관관계 히트맵 생성
        
        Args:
            data: 데이터
            title: 차트 제목
            height: 차트 높이
        
        Returns:
            Plotly 차트 JSON 데이터
        """
        try:
            # 숫자형 컬럼만 선택
            numeric_data = data.select_dtypes(include=[np.number])
            
            # 상관관계 계산
            corr_matrix = numeric_data.corr()
            
            # 히트맵 생성
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=np.round(corr_matrix.values, 2),
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            # 레이아웃 설정
            fig.update_layout(
                title=title,
                template=self.theme,
                height=height,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            logger.info(f"상관관계 히트맵 생성 완료: {corr_matrix.shape[0]}x{corr_matrix.shape[1]}")
            return json.loads(fig.to_json())
            
        except Exception as e:
            logger.error(f"상관관계 히트맵 생성 실패: {e}")
            raise
