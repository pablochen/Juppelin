// Juppelin Frontend JavaScript
// 코드 셀 관리 및 서버 통신

class JuppelinApp {
  constructor() {
    this.socket = null;
    this.cellCounter = 1;
    this.editors = new Map();
    this.executionCount = 0;

    this.init();
  }

  init() {
    this.setupSocketConnection();
    this.setupEventListeners();
    this.updateLastUpdate();
    this.checkStorageUsage();

    // 초기 셀 설정
    this.setupInitialCell();
  }

  setupSocketConnection() {
    this.socket = io();

    this.socket.on("connect", () => {
      console.log("Connected to server");
      this.updateConnectionStatus("connected", "서버 연결됨");
    });

    this.socket.on("disconnect", () => {
      console.log("Disconnected from server");
      this.updateConnectionStatus("disconnected", "서버 연결 끊김");
    });

    this.socket.on("status", (data) => {
      console.log("Server status:", data.message);
    });

    // 코드 실행 결과 수신
    this.socket.on("execution_result", (data) => {
      this.displayExecutionResult(data.cell_id, data);
    });

    // 차트 데이터 수신
    this.socket.on("chart_update", (data) => {
      this.displayChart(data);
    });
  }

  setupEventListeners() {
    // 셀 추가 버튼
    document.getElementById("add-cell-btn").addEventListener("click", () => {
      this.addNewCell();
    });

    // 차트 지우기 버튼
    document
      .querySelector(".btn-clear-charts")
      .addEventListener("click", () => {
        this.clearCharts();
      });

    // 키보드 단축키
    document.addEventListener("keydown", (e) => {
      this.handleKeyboardShortcuts(e);
    });
  }

  setupInitialCell() {
    const cellId = "cell-1";
    const editorElement = document.getElementById(`editor-${cellId}`);

    if (editorElement) {
      // 간단한 텍스트에어리어로 시작 (Monaco Editor는 나중에 통합)
      this.convertToEditableCell(cellId);
    }
  }

  convertToEditableCell(cellId) {
    const editorElement = document.getElementById(`editor-${cellId}`);
    const currentContent = editorElement.textContent;

    // 텍스트에어리어로 변환
    editorElement.innerHTML = "";
    const textarea = document.createElement("textarea");
    textarea.value = currentContent;
    textarea.className = "cell-textarea";
    textarea.style.cssText = `
            width: 100%;
            height: 100px;
            background: var(--bg-primary);
            color: var(--text-primary);
            border: none;
            outline: none;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            padding: 0;
            resize: vertical;
            line-height: 1.5;
        `;
    textarea.disabled = false;
    textarea.readOnly = false;
    editorElement.appendChild(textarea);
    this.editors.set(cellId, textarea);

    // Enter 키 처리
    textarea.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && (e.ctrlKey || e.shiftKey)) {
        e.preventDefault();
        this.runCell(cellId);
      }
    });
  }

  addNewCell() {
    this.cellCounter++;
    const cellId = `cell-${this.cellCounter}`;

    const cellHTML = `
            <div class="code-cell" data-cell-id="${cellId}">
                <div class="cell-header">
                    <span class="cell-number">[ ]:</span>
                    <div class="cell-controls">
                        <button class="btn-run" onclick="app.runCell('${cellId}')">실행</button>
                        <button class="btn-delete" onclick="app.deleteCell('${cellId}')">삭제</button>
                    </div>
                </div>
                <div class="cell-editor" id="editor-${cellId}">
# 새로운 셀
print("Hello from new cell!")
                </div>
                <div class="cell-output" id="output-${cellId}"></div>
            </div>
        `;

    const container = document.getElementById("cells-container");
    container.insertAdjacentHTML("beforeend", cellHTML);

    // 새 셀을 편집 가능하게 설정
    this.convertToEditableCell(cellId);

    // 새 셀로 스크롤
    const newCell = document.querySelector(`[data-cell-id="${cellId}"]`);
    newCell.scrollIntoView({ behavior: "smooth" });
  }

  async runCell(cellId) {
    const editor = this.editors.get(cellId);
    if (!editor) {
      console.error("Editor not found for cell:", cellId);
      return;
    }

    const code = editor.value.trim();
    if (!code) {
      return;
    }

    // 셀 번호 업데이트
    this.executionCount++;
    const cellNumber = document.querySelector(
      `[data-cell-id="${cellId}"] .cell-number`,
    );
    cellNumber.textContent = `[${this.executionCount}]:`;

    // 실행 중 표시
    this.showExecutionStatus(cellId, "running");

    try {
      // 서버에 코드 실행 요청
      const response = await fetch("/api/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cell_id: cellId,
          code: code,
          cell_type: "code",
        }),
      });

      const result = await response.json();
      this.displayExecutionResult(cellId, result);
    } catch (error) {
      console.error("Execution error:", error);
      this.displayExecutionResult(cellId, {
        status: "error",
        error_message: `네트워크 오류: ${error.message}`,
      });
    }
  }

  displayExecutionResult(cellId, result) {
    const outputElement = document.getElementById(`output-${cellId}`);

    if (result.status === "success") {
      let outputHTML = "";
      let dataFrameCount = 0;
      let lastDataFrame = null;
      let hasChart = false;
      
      if (result.outputs && result.outputs.length > 0) {
        result.outputs.forEach((output) => {
          if (output.output_type === "dataframe") {
            dataFrameCount++;
            lastDataFrame = output.data; // 마지막 DataFrame만 사용
          } else if (output.output_type === "stream") {
            const text = output.text;
            outputHTML += `<pre>${this.escapeHtml(text)}</pre>`;
            if (
              text.includes("plot") ||
              text.includes("chart") ||
              text.includes("figure")
            ) {
              hasChart = true;
            }
          } else if (output.output_type === "execute_result") {
            if (output.data && output.data["text/plain"]) {
              outputHTML += `<pre>${this.escapeHtml(output.data["text/plain"])}</pre>`;
            }
          }
        });
      }
      outputElement.innerHTML =
        outputHTML || "<pre>실행 완료 (출력 없음)</pre>";
      outputElement.className = "cell-output has-content";
      
      // DataFrame이 있으면 마지막 것만 한 번만 처리
      if (lastDataFrame) {
        this.addInteractiveDataFrameTab(lastDataFrame);
      } else if (hasChart) {
        this.addVisualizationTab(result.outputs, outputHTML);
      }
    } else {
      outputElement.innerHTML = `
                <div style="color: var(--accent-red);">
                    <strong>오류:</strong><br>
                    <pre>${this.escapeHtml(result.error_message || "알 수 없는 오류")}</pre>
                </div>
            `;
      outputElement.className = "cell-output has-content";
    }
    this.updateLastUpdate();
  }

  addInteractiveDataFrameTab(dfData) {
    const chartsContainer = document.getElementById("charts-container");
    
    // Welcome message 제거
    const welcomeMessage = chartsContainer.querySelector(".welcome-message");
    if (welcomeMessage) {
      welcomeMessage.remove();
    }
    
    // 탭 컨테이너가 없으면 생성
    let tabsContainer = chartsContainer.querySelector(".tabs-container");
    if (!tabsContainer) {
      tabsContainer = document.createElement("div");
      tabsContainer.className = "tabs-container";
      chartsContainer.appendChild(tabsContainer);
    }
    
    // 탭 헤더 생성
    let tabsHeader = tabsContainer.querySelector(".tabs-header");
    if (!tabsHeader) {
      tabsHeader = document.createElement("div");
      tabsHeader.className = "tabs-header";
      tabsContainer.appendChild(tabsHeader);
    }
    
    // 탭 콘텐츠 생성
    let tabsContent = tabsContainer.querySelector(".tabs-content");
    if (!tabsContent) {
      tabsContent = document.createElement("div");
      tabsContent.className = "tabs-content";
      tabsContainer.appendChild(tabsContent);
    }
    
    // DataFrame 내용의 해시를 생성해서 중복 확인
    const dfHash = this.generateDataFrameHash(dfData);
    const existingTab = Array.from(tabsContent.children).find(tab => 
      tab.dataset.dfHash === dfHash
    );
    
    if (existingTab) {
      // 이미 같은 내용의 탭이 있으면 그 탭을 활성화
      this.switchTab(existingTab.id);
      return;
    }
    
    // 새 탭 생성
    const tabId = `tab-${Date.now()}`;
    const tabTitle = `DataFrame ${tabsContent.children.length + 1}`;
    
    // 탭 버튼 생성
    const tabButton = document.createElement("button");
    tabButton.className = "tab-button";
    tabButton.textContent = tabTitle;
    tabButton.onclick = () => this.switchTab(tabId);
    tabsHeader.appendChild(tabButton);
    
    // 탭 콘텐츠 생성
    const tabContent = document.createElement("div");
    tabContent.className = "tab-content";
    tabContent.id = tabId;
    tabContent.dataset.dfHash = dfHash; // 해시 저장
    
    // 상호작용 DataFrame 표 렌더링
    tabContent.appendChild(this.renderInteractiveDataFrame(dfData));
    tabsContent.appendChild(tabContent);
    
    // 첫 번째 탭이면 활성화
    if (tabsContent.children.length === 1) {
      this.switchTab(tabId);
    }
  }
  
  generateDataFrameHash(dfData) {
    // DataFrame의 구조와 일부 데이터를 기반으로 간단한 해시 생성
    const structure = {
      columns: dfData.columns,
      indexName: dfData.index_name,
      rowCount: dfData.data.data.length,
      // 처음 몇 행의 데이터만 사용 (성능을 위해)
      sampleData: dfData.data.data.slice(0, 3)
    };
    return JSON.stringify(structure);
  }

  renderInteractiveDataFrame(dfData) {
    const container = document.createElement("div");
    container.className = "interactive-dataframe-container";
    
    // 데이터 준비 - 인덱스를 첫 번째 컬럼으로 추가
    const allColumns = ['Index', ...dfData.columns];
    const allData = dfData.data.data.map((row, i) => [dfData.data.index[i], ...row]);
    
    // 상태 관리
    const state = {
      currentPage: 0,
      pageSize: 20,
      sortColumn: null,
      sortDirection: 'asc',
      filterText: '',
      data: allData,
      columns: allColumns,
      filteredData: allData
    };
    
    // 컨테이너 HTML 구조
    container.innerHTML = `
      <div class="df-controls">
        <div class="df-info">
          <span class="df-shape">Shape: ${allData.length} rows × ${allColumns.length} columns</span>
        </div>
        <div class="df-actions">
          <input type="text" class="df-filter" placeholder="필터링..." />
          <select class="df-pagesize">
            <option value="10">10 rows</option>
            <option value="20" selected>20 rows</option>
            <option value="50">50 rows</option>
            <option value="100">100 rows</option>
          </select>
        </div>
      </div>
      <div class="df-table-wrapper">
        <table class="df-table">
          <thead></thead>
          <tbody></tbody>
        </table>
      </div>
      <div class="df-pagination">
        <button class="df-prev" disabled>이전</button>
        <span class="df-page-info"></span>
        <button class="df-next">다음</button>
      </div>
    `;
    
    // 이벤트 리스너 설정
    const filterInput = container.querySelector('.df-filter');
    const pageSizeSelect = container.querySelector('.df-pagesize');
    const prevBtn = container.querySelector('.df-prev');
    const nextBtn = container.querySelector('.df-next');
    
    // 필터링 기능
    filterInput.addEventListener('input', (e) => {
      state.filterText = e.target.value.toLowerCase();
      state.filteredData = state.data.filter(row => 
        row.some(cell => String(cell).toLowerCase().includes(state.filterText))
      );
      state.currentPage = 0;
      updateTable();
    });
    
    // 페이지 크기 변경
    pageSizeSelect.addEventListener('change', (e) => {
      state.pageSize = parseInt(e.target.value);
      state.currentPage = 0;
      updateTable();
    });
    
    // 페이지네이션
    prevBtn.addEventListener('click', () => {
      if (state.currentPage > 0) {
        state.currentPage--;
        updateTable();
      }
    });
    
    nextBtn.addEventListener('click', () => {
      const maxPage = Math.ceil(state.filteredData.length / state.pageSize) - 1;
      if (state.currentPage < maxPage) {
        state.currentPage++;
        updateTable();
      }
    });
    
    // 테이블 업데이트 함수
    const updateTable = () => {
      const thead = container.querySelector('thead');
      const tbody = container.querySelector('tbody');
      
      // 헤더 생성
      thead.innerHTML = '';
      const headerRow = document.createElement('tr');
      state.columns.forEach((col, index) => {
        const th = document.createElement('th');
        th.textContent = col;
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => sortByColumn(index));
        
        // 정렬 표시
        if (state.sortColumn === index) {
          th.textContent += state.sortDirection === 'asc' ? ' ↑' : ' ↓';
        }
        
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);
      
      // 데이터 정렬
      if (state.sortColumn !== null) {
        state.filteredData.sort((a, b) => {
          const aVal = a[state.sortColumn];
          const bVal = b[state.sortColumn];
          
          // 숫자 비교
          if (!isNaN(aVal) && !isNaN(bVal)) {
            return state.sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
          }
          
          // 문자열 비교
          const result = String(aVal).localeCompare(String(bVal));
          return state.sortDirection === 'asc' ? result : -result;
        });
      }
      
      // 페이지네이션된 데이터
      const startIndex = state.currentPage * state.pageSize;
      const endIndex = startIndex + state.pageSize;
      const pageData = state.filteredData.slice(startIndex, endIndex);
      
      // 바디 생성
      tbody.innerHTML = '';
      pageData.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach(cell => {
          const td = document.createElement('td');
          td.textContent = cell;
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
      
      // 페이지네이션 정보 업데이트
      const totalPages = Math.ceil(state.filteredData.length / state.pageSize);
      const pageInfo = container.querySelector('.df-page-info');
      pageInfo.textContent = `${state.currentPage + 1} / ${totalPages} 페이지 (총 ${state.filteredData.length}행)`;
      
      // 버튼 상태 업데이트
      prevBtn.disabled = state.currentPage === 0;
      nextBtn.disabled = state.currentPage >= totalPages - 1;
    };
    
    // 정렬 함수
    const sortByColumn = (columnIndex) => {
      if (state.sortColumn === columnIndex) {
        state.sortDirection = state.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        state.sortColumn = columnIndex;
        state.sortDirection = 'asc';
      }
      updateTable();
    };
    
    // 초기 테이블 렌더링
    updateTable();
    
    // CSS 스타일 추가
    const style = document.createElement('style');
    style.textContent = `
      .interactive-dataframe-container {
        font-family: monospace;
        margin: 10px 0;
      }
      .df-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        padding: 10px;
        background: var(--bg-secondary);
        border-radius: 4px;
      }
      .df-actions {
        display: flex;
        gap: 10px;
      }
      .df-filter, .df-pagesize {
        padding: 5px;
        border: 1px solid var(--border-color);
        border-radius: 3px;
        background: var(--bg-primary);
        color: var(--text-primary);
      }
      .df-table-wrapper {
        max-height: 400px;
        overflow: auto;
        border: 1px solid var(--border-color);
        border-radius: 4px;
      }
      .df-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
      }
      .df-table th {
        background: var(--bg-secondary);
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
        position: sticky;
        top: 0;
        user-select: none;
      }
      .df-table th:hover {
        background: var(--accent-blue);
      }
      .df-table td {
        padding: 6px 8px;
        border-bottom: 1px solid var(--border-color);
        white-space: nowrap;
      }
      .df-table tr:nth-child(even) {
        background: var(--bg-secondary);
      }
      .df-pagination {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px;
        padding: 10px;
      }
      .df-prev, .df-next {
        padding: 5px 15px;
        border: 1px solid var(--border-color);
        border-radius: 3px;
        background: var(--bg-primary);
        color: var(--text-primary);
        cursor: pointer;
      }
      .df-prev:disabled, .df-next:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      .df-page-info {
        font-size: 14px;
        color: var(--text-secondary);
      }
    `;
    
    if (!document.querySelector('#interactive-df-styles')) {
      style.id = 'interactive-df-styles';
      document.head.appendChild(style);
    }
    
    return container;
  }

  deleteCell(cellId) {
    if (this.editors.size <= 1) {
      alert("마지막 셀은 삭제할 수 없습니다.");
      return;
    }

    const cell = document.querySelector(`[data-cell-id="${cellId}"]`);
    if (cell) {
      cell.remove();
      this.editors.delete(cellId);
    }
  }

  showExecutionStatus(cellId, status) {
    const outputElement = document.getElementById(`output-${cellId}`);

    if (status === "running") {
      outputElement.innerHTML = "<pre>실행 중...</pre>";
      outputElement.className = "cell-output has-content";
    }
  }

  displayChart(chartData) {
    const chartsContainer = document.getElementById("charts-container");

    // Welcome message 제거
    const welcomeMessage = chartsContainer.querySelector(".welcome-message");
    if (welcomeMessage) {
      welcomeMessage.remove();
    }

    // 새 차트 컨테이너 생성
    const chartContainer = document.createElement("div");
    chartContainer.className = "chart-container";
    chartContainer.innerHTML = `
            <div class="chart-title">${chartData.title || "차트"}</div>
            <div class="chart-plot" id="chart-${Date.now()}"></div>
        `;

    chartsContainer.appendChild(chartContainer);

    // Plotly 차트 렌더링 (실제 구현은 나중에)
    const plotElement = chartContainer.querySelector(".chart-plot");
    plotElement.innerHTML = "<p>차트가 여기에 표시됩니다.</p>";
  }

  addVisualizationTab(outputs, fullText) {
    const chartsContainer = document.getElementById("charts-container");

    // Welcome message 제거
    const welcomeMessage = chartsContainer.querySelector(".welcome-message");
    if (welcomeMessage) {
      welcomeMessage.remove();
    }

    // 탭 컨테이너가 없으면 생성
    let tabsContainer = chartsContainer.querySelector(".tabs-container");
    if (!tabsContainer) {
      tabsContainer = document.createElement("div");
      tabsContainer.className = "tabs-container";
      chartsContainer.appendChild(tabsContainer);
    }

    // 탭 헤더 생성
    let tabsHeader = tabsContainer.querySelector(".tabs-header");
    if (!tabsHeader) {
      tabsHeader = document.createElement("div");
      tabsHeader.className = "tabs-header";
      tabsContainer.appendChild(tabsHeader);
    }

    // 탭 콘텐츠 생성
    let tabsContent = tabsContainer.querySelector(".tabs-content");
    if (!tabsContent) {
      tabsContent = document.createElement("div");
      tabsContent.className = "tabs-content";
      tabsContainer.appendChild(tabsContent);
    }

    // 새 탭 생성
    const tabId = `tab-${Date.now()}`;
    const tabTitle = `결과 ${tabsContent.children.length + 1}`;

    // 탭 버튼 생성
    const tabButton = document.createElement("button");
    tabButton.className = "tab-button";
    tabButton.textContent = tabTitle;
    tabButton.onclick = () => this.switchTab(tabId);
    tabsHeader.appendChild(tabButton);

    // 탭 콘텐츠 생성
    const tabContent = document.createElement("div");
    tabContent.className = "tab-content";
    tabContent.id = tabId;

    // 마지막 DataFrame 출력만 찾기
    let contentHTML = "";
    let hasDataFrame = false;
    let hasChart = false;
    let lastDataFrameText = "";

    // 마지막 DataFrame 출력 찾기
    for (let i = outputs.length - 1; i >= 0; i--) {
      const output = outputs[i];
      if (output.output_type === "stream") {
        const text = output.text;

        // DataFrame 감지 (마지막 것만)
        if (
          text.includes("DataFrame Head:") &&
          text.includes("timestamp") &&
          text.includes("open")
        ) {
          hasDataFrame = true;
          lastDataFrameText = text;
          break; // 마지막 DataFrame만 사용
        }

        // 차트 감지
        if (
          text.includes("plot") ||
          text.includes("chart") ||
          text.includes("figure")
        ) {
          hasChart = true;
          contentHTML += this.createChartPlaceholder(text);
          break; // 마지막 차트만 사용
        }
      }
    }

    // DataFrame이 있으면 마지막 것만 표시
    if (hasDataFrame) {
      contentHTML += this.createDataFrameTable(lastDataFrameText);
    }

    tabContent.innerHTML = contentHTML;
    tabsContent.appendChild(tabContent);

    // 첫 번째 탭이면 활성화
    if (tabsContent.children.length === 1) {
      this.switchTab(tabId);
    }
  }

  createDataFrameTable(text) {
    // DataFrame 텍스트를 파싱하여 테이블로 변환 (컬럼별로 정확히 분리)
    let tableHTML = '<div class="dataframe-container">';
    tableHTML += "<h4>DataFrame 결과</h4>";
    tableHTML += '<div class="table-wrapper">';
    tableHTML += '<table class="dataframe-table">';

    // DataFrame 정보 추출
    let columns = [];
    let dataRows = [];

    // DataFrame Head 섹션에서 실제 데이터만 추출
    const lines = text.split("\n");
    let inDataSection = false;
    let headerFound = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      // DataFrame Head 섹션 시작
      if (line.includes("DataFrame Head:")) {
        inDataSection = true;
        continue;
      }
      // DataFrame 출력 끝
      if (inDataSection && line.match(/^\[\d+ rows x \d+ columns\]$/)) {
        break;
      }
      // DataFrame 출력 부분에서만 파싱
      if (inDataSection && line.trim()) {
        // 컬럼 헤더 찾기 (timestamp로 시작하고 open, high가 포함된 행)
        if (
          !headerFound &&
          line.includes("timestamp") &&
          line.includes("open") &&
          line.includes("high")
        ) {
          // 컬럼명 추출 (공백 기준, 인덱스 컬럼 포함)
          const parts = line.split(/\s{2,}/).filter((part) => part.length > 0);
          columns = parts;
          headerFound = true;
          continue;
        }
        // 데이터 행 찾기 (날짜로 시작하는 행)
        if (headerFound && /^\d{4}-\d{2}-\d{2}/.test(line)) {
          // 인덱스(날짜+시간)와 값 분리 (공백 2개 이상 기준)
          const parts = line.split(/\s{2,}/).filter((part) => part.length > 0);
          if (parts.length === columns.length) {
            dataRows.push(parts);
          }
        }
      }
    }

    // 헤더 생성
    tableHTML += "<thead><tr>";
    columns.forEach((col) => {
      tableHTML += `<th>${col}</th>`;
    });
    tableHTML += "</tr></thead>";

    // 데이터 행 생성
    tableHTML += "<tbody>";
    dataRows.forEach((row) => {
      tableHTML += "<tr>";
      row.forEach((value) => {
        tableHTML += `<td>${value}</td>`;
      });
      tableHTML += "</tr>";
    });

    // 데이터가 없으면 원본 텍스트 표시
    if (dataRows.length === 0) {
      tableHTML += `<tr><td colspan="${Math.max(columns.length, 2)}">`;
      tableHTML += `<pre style="font-size: 11px; color: var(--text-secondary);">${this.escapeHtml(text)}</pre>`;
      tableHTML += "</td></tr>";
    }

    tableHTML += "</tbody>";
    tableHTML += "</table>";
    tableHTML += "</div>";
    tableHTML += "</div>";
    return tableHTML;
    return tableHTML;
  }

  createChartPlaceholder(text) {
    return `
            <div class="chart-container">
                <h4>차트 결과</h4>
                <div class="chart-placeholder">
                    <p>차트가 여기에 표시됩니다</p>
                    <div class="chart-info">
                        <small>출력: ${this.escapeHtml(text.substring(0, 100))}...</small>
                    </div>
                </div>
            </div>
        `;
  }

  switchTab(tabId) {
    const tabsContainer = document.querySelector(".tabs-container");
    if (!tabsContainer) return;

    // 모든 탭 버튼 비활성화
    const tabButtons = tabsContainer.querySelectorAll(".tab-button");
    tabButtons.forEach((btn) => btn.classList.remove("active"));

    // 모든 탭 콘텐츠 숨기기
    const tabContents = tabsContainer.querySelectorAll(".tab-content");
    tabContents.forEach((content) => (content.style.display = "none"));

    // 선택된 탭 활성화
    const selectedButton = tabsContainer.querySelector(
      `button[onclick*="${tabId}"]`,
    );
    if (selectedButton) {
      selectedButton.classList.add("active");
    }

    const selectedContent = document.getElementById(tabId);
    if (selectedContent) {
      selectedContent.style.display = "block";
    }
  }

  clearCharts() {
    const chartsContainer = document.getElementById("charts-container");
    chartsContainer.innerHTML = `
            <div class="welcome-message">
                <h4>📊 시각화 영역</h4>
                <p>코드를 실행하면 여기에 차트가 표시됩니다.</p>
                <div class="example-code">
                    <h5>예제 코드:</h5>
                    <pre><code># 데이터 수집
data = load_binance_data('BTCUSDT', '2025-01-01', 30)

# 시각화
plot_candlestick(data)</code></pre>
                </div>
            </div>
        `;
  }

  handleKeyboardShortcuts(e) {
    // Ctrl+Enter: 현재 포커스된 셀 실행
    if (e.ctrlKey && e.key === "Enter") {
      e.preventDefault();
      const focusedElement = document.activeElement;
      if (focusedElement.className === "cell-textarea") {
        const cellElement = focusedElement.closest(".code-cell");
        if (cellElement) {
          const cellId = cellElement.getAttribute("data-cell-id");
          this.runCell(cellId);
        }
      }
    }
  }

  updateConnectionStatus(status, message) {
    const statusElement = document.getElementById("connection-status");
    statusElement.textContent = message;
    statusElement.className = `status-item ${status}`;
  }

  updateLastUpdate() {
    const now = new Date();
    document.getElementById("last-update").textContent =
      now.toLocaleTimeString("ko-KR");
  }

  async checkStorageUsage() {
    try {
      const response = await fetch("/api/storage-usage");
      const data = await response.json();
      document.getElementById("storage-usage").textContent =
        data.usage || "계산 중...";
    } catch (error) {
      document.getElementById("storage-usage").textContent = "알 수 없음";
    }
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
}

// 전역 함수들 (HTML onclick에서 사용)
let app;

function runCell(cellId) {
  app.runCell(cellId);
}

function deleteCell(cellId) {
  app.deleteCell(cellId);
}

// 앱 초기화
document.addEventListener("DOMContentLoaded", () => {
  app = new JuppelinApp();
  console.log("Juppelin app initialized");
});
