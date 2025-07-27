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
        
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.updateConnectionStatus('connected', '서버 연결됨');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.updateConnectionStatus('disconnected', '서버 연결 끊김');
        });
        
        this.socket.on('status', (data) => {
            console.log('Server status:', data.message);
        });
        
        // 코드 실행 결과 수신
        this.socket.on('execution_result', (data) => {
            this.displayExecutionResult(data.cell_id, data);
        });
        
        // 차트 데이터 수신
        this.socket.on('chart_update', (data) => {
            this.displayChart(data);
        });
    }
    
    setupEventListeners() {
        // 셀 추가 버튼
        document.getElementById('add-cell-btn').addEventListener('click', () => {
            this.addNewCell();
        });
        
        // 차트 지우기 버튼
        document.querySelector('.btn-clear-charts').addEventListener('click', () => {
            this.clearCharts();
        });
        
        // 키보드 단축키
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
    }
    
    setupInitialCell() {
        const cellId = 'cell-1';
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
        editorElement.innerHTML = '';
        const textarea = document.createElement('textarea');
        textarea.value = currentContent;
        textarea.className = 'cell-textarea';
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
        
        editorElement.appendChild(textarea);
        this.editors.set(cellId, textarea);
        
        // Enter 키 처리
        textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.shiftKey)) {
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
        
        const container = document.getElementById('cells-container');
        container.insertAdjacentHTML('beforeend', cellHTML);
        
        // 새 셀을 편집 가능하게 설정
        this.convertToEditableCell(cellId);
        
        // 새 셀로 스크롤
        const newCell = document.querySelector(`[data-cell-id="${cellId}"]`);
        newCell.scrollIntoView({ behavior: 'smooth' });
    }
    
    async runCell(cellId) {
        const editor = this.editors.get(cellId);
        if (!editor) {
            console.error('Editor not found for cell:', cellId);
            return;
        }
        
        const code = editor.value.trim();
        if (!code) {
            return;
        }
        
        // 셀 번호 업데이트
        this.executionCount++;
        const cellNumber = document.querySelector(`[data-cell-id="${cellId}"] .cell-number`);
        cellNumber.textContent = `[${this.executionCount}]:`;
        
        // 실행 중 표시
        this.showExecutionStatus(cellId, 'running');
        
        try {
            // 서버에 코드 실행 요청
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    cell_id: cellId,
                    code: code,
                    cell_type: 'code'
                })
            });
            
            const result = await response.json();
            this.displayExecutionResult(cellId, result);
            
        } catch (error) {
            console.error('Execution error:', error);
            this.displayExecutionResult(cellId, {
                status: 'error',
                error_message: `네트워크 오류: ${error.message}`
            });
        }
    }
    
    displayExecutionResult(cellId, result) {
        const outputElement = document.getElementById(`output-${cellId}`);
        
        if (result.status === 'success') {
            let outputHTML = '';
            
            if (result.outputs && result.outputs.length > 0) {
                result.outputs.forEach(output => {
                    if (output.output_type === 'stream') {
                        outputHTML += `<pre>${this.escapeHtml(output.text)}</pre>`;
                    } else if (output.output_type === 'execute_result') {
                        if (output.data && output.data['text/plain']) {
                            outputHTML += `<pre>${this.escapeHtml(output.data['text/plain'])}</pre>`;
                        }
                    }
                });
            }
            
            outputElement.innerHTML = outputHTML || '<pre>실행 완료 (출력 없음)</pre>';
            outputElement.className = 'cell-output has-content';
            
        } else {
            // 오류 표시
            outputElement.innerHTML = `
                <div style="color: var(--accent-red);">
                    <strong>오류:</strong><br>
                    <pre>${this.escapeHtml(result.error_message || '알 수 없는 오류')}</pre>
                </div>
            `;
            outputElement.className = 'cell-output has-content';
        }
        
        this.updateLastUpdate();
    }
    
    deleteCell(cellId) {
        if (this.editors.size <= 1) {
            alert('마지막 셀은 삭제할 수 없습니다.');
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
        
        if (status === 'running') {
            outputElement.innerHTML = '<pre>실행 중...</pre>';
            outputElement.className = 'cell-output has-content';
        }
    }
    
    displayChart(chartData) {
        const chartsContainer = document.getElementById('charts-container');
        
        // Welcome message 제거
        const welcomeMessage = chartsContainer.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        // 새 차트 컨테이너 생성
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container';
        chartContainer.innerHTML = `
            <div class="chart-title">${chartData.title || '차트'}</div>
            <div class="chart-plot" id="chart-${Date.now()}"></div>
        `;
        
        chartsContainer.appendChild(chartContainer);
        
        // Plotly 차트 렌더링 (실제 구현은 나중에)
        const plotElement = chartContainer.querySelector('.chart-plot');
        plotElement.innerHTML = '<p>차트가 여기에 표시됩니다.</p>';
    }
    
    clearCharts() {
        const chartsContainer = document.getElementById('charts-container');
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
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            const focusedElement = document.activeElement;
            if (focusedElement.className === 'cell-textarea') {
                const cellElement = focusedElement.closest('.code-cell');
                if (cellElement) {
                    const cellId = cellElement.getAttribute('data-cell-id');
                    this.runCell(cellId);
                }
            }
        }
    }
    
    updateConnectionStatus(status, message) {
        const statusElement = document.getElementById('connection-status');
        statusElement.textContent = message;
        statusElement.className = `status-item ${status}`;
    }
    
    updateLastUpdate() {
        const now = new Date();
        document.getElementById('last-update').textContent = 
            now.toLocaleTimeString('ko-KR');
    }
    
    async checkStorageUsage() {
        try {
            const response = await fetch('/api/storage-usage');
            const data = await response.json();
            document.getElementById('storage-usage').textContent = 
                data.usage || '계산 중...';
        } catch (error) {
            document.getElementById('storage-usage').textContent = '알 수 없음';
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
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
document.addEventListener('DOMContentLoaded', () => {
    app = new JuppelinApp();
    console.log('Juppelin app initialized');
});
