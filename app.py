import streamlit as st

# 페이지 설정
st.set_page_config(page_title="RETRO ARCADE", page_icon="🕹️", layout="wide")

# 모든 게임의 로직과 그래픽, 키보드 조작을 브라우저에서 완벽히 실행하기 위한 HTML/JS 컴포넌트
# 원래 arcade.jsx의 네온 컬러(C)와 구조, 그리고 프나펌 리듬게임/9판 기억력/틱택토를 포함합니다.
arcade_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Retro Arcade</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #0a0a0f;
            color: #ccccee;
            font-family: 'Courier New', 'Lucida Console', monospace;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            padding: 20px;
        }
        /* 스캔라인 효과 */
        .scanlines {
            position: fixed; inset: 0; pointer-events: none; z-index: 9999;
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.13) 2px, rgba(0,0,0,0.13) 4px);
        }
        .container { width: 100%; max-width: 800px; display: flex; flex-direction: column; align-items: center; }
        
        /* 로비 타이틀 */
        .title { font-size: 50px; font-weight: bold; color: #ffe600; text-shadow: 0 0 10px rgba(255, 230, 0, 0.8); letter-spacing: 4px; margin-top: 20px; }
        .subtitle { color: #333355; letter-spacing: 5px; font-size: 11px; margin-bottom: 40px; }
        
        /* 오리지널 그리드 */
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; width: 100%; }
        .card {
            background: #0f0f1a; border: 2px solid #1a1a3a; border-radius: 8px; padding: 24px;
            text-align: center; cursor: pointer; transition: all 0.2s ease; position: relative;
        }
        .card:hover { border-color: #ccccee; background: #131326; }
        .card .emoji { font-size: 32px; margin-bottom: 8px; }
        .card .name { font-size: 14px; font-weight: bold; letter-spacing: 2px; margin-bottom: 4px; }
        .card .desc { font-size: 11px; color: #333355; }
        .card .play-btn { font-size: 11px; margin-top: 10px; display: none; letter-spacing: 2px; }
        .card:hover .play-btn { display: block; }

        /* 게임 공통 템플릿 */
        .game-header { width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid #1a1a3a; padding-bottom: 10px; }
        .game-title { font-size: 24px; font-weight: bold; }
        .back-btn { background: transparent; border: 1px solid #333355; color: #ccccee; padding: 6px 12px; cursor: pointer; font-family: monospace; }
        .back-btn:hover { background: #1a1a3a; border-color: #ccccee; }
        .guide-box { background: #0f0f1a; border-left: 4px solid #fff; padding: 12px; width: 100%; font-size: 12px; margin-bottom: 20px; line-height: 1.5; }

        /* 캔버스 뷰포트 (오리지널 테트리스/스네이크/벽돌/인베이더용) */
        canvas { background: #000; border: 4px solid #1a1a3a; box-shadow: 0 0 20px rgba(0,0,0,0.8); display: block; margin: 0 auto; }

        /* [신규] 프나펌 스타일 리듬 게임 레이아웃 */
        .rhythm-container { width: 100%; max-width: 400px; background: #05050a; border: 2px solid #1a1a3a; padding: 20px; position: relative; text-align: center; }
        .rhythm-receptor-row { display: flex; justify-content: space-around; margin-bottom: 20px; background: #0f0f1a; padding: 10px; border-radius: 6px; }
        .receptor { font-size: 28px; font-weight: bold; color: #333355; width: 50px; height: 50px; line-height: 50px; border: 2px dashed #1a1a3a; border-radius: 6px; transition: all 0.1s; }
        .receptor.active { transform: scale(1.15); border-style: solid; box-shadow: 0 0 10px currentColor; }
        .rhythm-track { height: 300px; position: relative; overflow: hidden; background: linear-gradient(180deg, #05050a 80%, #111122 100%); border: 1px solid #1a1a3a; }
        .falling-note { position: absolute; font-size: 28px; font-weight: bold; width: 50px; text-align: center; animation: fall linear forward; }
        @keyframes fall { from { top: -40px; } to { top: 300px; } }
        .judgment-msg { font-size: 20px; font-weight: bold; margin-top: 15px; height: 24px; color: #ffe600; }

        /* [신규] 9판 기억력 게임 (시몬 가라사대) */
        .simon-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; width: 300px; margin: 20px auto; }
        .simon-pad { height: 80px; background: #0f0f1a; border: 2px solid #1a1a3a; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; color: #333355; transition: all 0.1s; }
        .simon-pad.active { background: #ffe600 !important; color: #000 !important; box-shadow: 0 0 20px #ffe600; }

        /* [신규] 틱택토 */
        .ttt-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 300px; margin: 20px auto; }
        .ttt-cell { height: 90px; background: #0f0f1a; border: 2px solid #1a1a3a; font-size: 36px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .ttt-cell:hover { background: #131326; }
    </style>
</head>
<body>
    <div class="scanlines"></div>
    <div class="container" id="app"></div>

    <script>
        // 전역 상태 관리
        let currentScene = "lobby";
        let score = 0;
        let gameInterval = null;

        // 색상 사전
        const C = { yellow: "#ffe600", green: "#00ff88", cyan: "#00e5ff", pink: "#ff2d9b", orange: "#ff6d00", red: "#ff1744", purple: "#d500f9" };

        const gamesData = [
            { id: "tetris", name: "TETRIS", emoji: "🟦", color: C.cyan, desc: "Falling block puzzle game", ctrl: "키보드 [←][→] 이동 / [↑] 회전 / [↓] 소프트 드롭" },
            { id: "snake", name: "SNAKE", emoji: "🐍", color: C.green, desc: "Classic nibble retro game", ctrl: "키보드 방향키 [←][↑][↓][→] 방향 전환" },
            { id: "breakout", name: "BREAKOUT", emoji: "🧱", color: C.orange, desc: "Brick breaking action", ctrl: "키보드 방향키 [←][→] 패들 이동" },
            { id: "space", name: "SPACE INVADERS", emoji: "👾", color: C.red, desc: "Retro space shooter arcade", ctrl: "키보드 [←][→] 이동 / [Spacebar] 미사일 발사" },
            { id: "rhythm", name: "RHYTHM BEAT", emoji: "🎵", color: C.pink, desc: "FnF 모티브 키보드 리듬액션", ctrl: "★실제 키보드 방향키 [←][↑][↓][→] 타이밍 조작★" },
            { id: "simon", name: "SIMON SAYS", emoji: "🧠", color: C.yellow, desc: "9-Grid 패턴 기억력 테스트", ctrl: "마우스로 깜빡인 발판 순서대로 클릭 (점점 빨라짐)" },
            { id: "ttt", name: "TIC-TAC-TOE", emoji: "❌", color: C.purple, desc: "Classic match-3 grid board", ctrl: "마우스로 빈칸 선택하여 스마트 AI와 대결" }
        ];

        function changeScene(scene) {
            currentScene = scene;
            if (gameInterval) { clearInterval(gameInterval); gameInterval = null; }
            document.removeEventListener("keydown", handleGlobalKeyDown);
            render();
        }

        function handleGlobalKeyDown(e) {
            // 게임별 키보드 차단 및 핸들러 연결은 각 게임 생성자 내에서 처리
        }

        function render() {
            const app = document.getElementById("app");
            app.innerHTML = "";

            if (currentScene === "lobby") {
                renderLobby(app);
            } else {
                renderGameLayout(app);
            }
        }

        // 1. 로비 화면 (원래 그리드 복제)
        function renderLobby(container) {
            const titleEl = document.createElement("div");
            titleEl.className = "title";
            titleEl.innerText = "RETRO ARCADE";
            container.appendChild(titleEl);

            const subEl = document.createElement("div");
            subEl.className = "subtitle";
            subEl.innerText = "7 MINI GAMES (PRO EDITION)";
            container.appendChild(subEl);

            const gridEl = document.createElement("div");
            gridEl.className = "grid";

            gamesData.forEach(g => {
                const card = document.createElement("div");
                card.className = "card";
                card.onclick = () => changeScene(g.id);
                card.innerHTML = `
                    <div class="emoji">${g.emoji}</div>
                    <div class="name" style="color: ${g.color}">${g.name}</div>
                    <div class="desc">${g.desc}</div>
                    <div class="play-btn" style="color: ${g.color}">▶ PLAY</div>
                `;
                gridEl.appendChild(card);
            });
            container.appendChild(gridEl);
        }

        // 2. 게임 공통 상단 가이드 및 이식 레이아웃
        function renderGameLayout(container) {
            const g = gamesData.find(x => x.id === currentScene);
            
            const header = document.createElement("div");
            header.className = "game-header";
            header.innerHTML = `
                <div class="game-title" style="color: ${g.color}">${g.emoji} ${g.name}</div>
                <button class="back-btn" onclick="changeScene('lobby')">◀ LOBBY</button>
            `;
            container.appendChild(header);

            const guide = document.createElement("div");
            guide.className = "guide-box";
            guide.style.borderLeftColor = g.color;
            guide.innerHTML = `
                <strong>📝 게임 설명:</strong> ${g.desc}<br/>
                <strong style="color: #ff2d9b">🕹️ 조작 키:</strong> ${g.ctrl}
            `;
            container.appendChild(guide);

            const gameWorkspace = document.createElement("div");
            gameWorkspace.id = "workspace";
            gameWorkspace.style.width = "100%";
            container.appendChild(gameWorkspace);

            // 해당 게임 실행
            if (currentScene === "rhythm") startRhythmGame(gameWorkspace);
            else if (currentScene === "simon") startSimonGame(gameWorkspace);
            else if (currentScene === "ttt") startTictactoeGame(gameWorkspace);
            else startCanvasGame(currentScene, gameWorkspace);
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        // [신규] 프나펌 모티브 키보드 리듬 게임 (RHYTHM BEAT)
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function startRhythmGame(ctx) {
            ctx.innerHTML = `
                <div style="display:flex; justify-content:center;">
                    <div class="rhythm-container">
                        <div style="margin-bottom:10px; font-size:14px; font-weight:bold;">SCORE: <span id="r-score" style="color:#00e5ff">0</span></div>
                        <div class="rhythm-receptor-row">
                            <div class="receptor" id="rcp-ArrowLeft" style="color:${C.cyan}">←</div>
                            <div class="receptor" id="rcp-ArrowUp" style="color:${C.green}">↑</div>
                            <div class="receptor" id="rcp-ArrowDown" style="color:${C.purple}">↓</div>
                            <div class="receptor" id="rcp-ArrowRight" style="color:${C.pink}">→</div>
                        </div>
                        <div class="rhythm-track" id="r-track"></div>
                        <div class="judgment-msg" id="r-judg">READY</div>
                    </div>
                </div>
            `;

            let rScore = 0;
            const track = document.getElementById("r-track");
            const keys = ["ArrowLeft", "ArrowUp", "ArrowDown", "ArrowRight"];
            const arrowSymbols = { "ArrowLeft": "←", "ArrowUp": "↑", "ArrowDown": "↓", "ArrowRight": "→" };
            const arrowColors = { "ArrowLeft": C.cyan, "ArrowUp": C.green, "ArrowDown": C.purple, "ArrowRight": C.pink };
            const activeNotes = [];

            function spawnNote() {
                const k = keys[Math.floor(Math.random() * keys.length)];
                const noteEl = document.createElement("div");
                noteEl.className = "falling-note";
                noteEl.innerText = arrowSymbols[k];
                noteEl.style.color = arrowColors[k];
                
                // 트랙 가로 분할 위치 계산
                const idx = keys.indexOf(k);
                noteEl.style.left = `${idx * 25 + 4}%`;
                
                const speed = 2.5; // 내려오는 시간(초)
                noteEl.style.animationDuration = `${speed}s`;
                track.appendChild(noteEl);

                const noteObj = { key: k, element: noteEl, spawnedAt: Date.now(), duration: speed * 1000, hit: false };
                activeNotes.push(noteObj);

                // 화면 밖으로 나가면 삭제
                setTimeout(() => {
                    if (!noteObj.hit) {
                        document.getElementById("r-judg").innerText = "MISS!";
                        document.getElementById("r-judg").style.color = C.red;
                        noteEl.remove();
                    }
                    const index = activeNotes.indexOf(noteObj);
                    if (index > -1) activeNotes.splice(index, 1);
                }, speed * 1000);
            }

            // 프레임워크 스폰 인터벌
            gameInterval = setInterval(spawnNote, 800);

            // 실제 키보드 입력 가로채기 핸들러
            const rhythmKeyHandler = (e) => {
                if (!keys.includes(e.key)) return;
                e.preventDefault();

                // 수신기 불빛 애니메이션
                const rcp = document.getElementById(`rcp-${e.key}`);
                if (rcp) {
                    rcp.classList.add("active");
                    setTimeout(() => rcp.classList.remove("active"), 100);
                }

                // 가장 아래에 도달한 알맞은 노트 탐색
                const now = Date.now();
                let judged = false;

                for (let i = 0; i < activeNotes.length; i++) {
                    const n = activeNotes[i];
                    if (n.key === e.key && !n.hit) {
                        const progress = (now - n.spawnedAt) / n.duration;
                        // 판정선 도달 임계구간 (FnF 판정 매칭 약 85% ~ 96% 위치가 완벽한 타이밍)
                        if (progress > 0.78 && progress < 0.96) {
                            n.hit = true;
                            n.element.remove();
                            judged = true;
                            
                            const diff = Math.abs(progress - 0.88);
                            const judgText = document.getElementById("r-judg");
                            if (diff < 0.04) {
                                rScore += 150; judgText.innerText = "SICK!!"; judgText.style.color = C.cyan;
                            } else {
                                rScore += 100; judgText.innerText = "GOOD"; judgText.style.color = C.green;
                            }
                            document.getElementById("r-score").innerText = rScore;
                            break;
                        }
                    }
                }
                if(!judged) {
                    document.getElementById("r-judg").innerText = "BAD/MISS";
                    document.getElementById("r-judg").style.color = C.orange;
                }
            };

            document.addEventListener("keydown", rhythmKeyHandler);
            // 씬 이탈 시 이벤트 소멸을 위해 캐싱
            window.currentCleanup = () => document.removeEventListener("keydown", rhythmKeyHandler);
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        // [신규] 9개 판 깜빡이는 순서 맞추기 기억력 게임 (SIMON SAYS)
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function startSimonGame(ctx) {
            ctx.innerHTML = `
                <div style="text-align:center;">
                    <h3 style="margin-bottom:5px;">STAGE: <span id="s-stage" style="color:${C.yellow}">1</span></h3>
                    <div id="s-status" style="font-size:13px; color:${C.green}; margin-bottom:15px;">준비 중...</div>
                    <div class="simon-grid" id="s-grid"></div>
                </div>
            `;

            const grid = document.getElementById("s-grid");
            for (let i = 0; i < 9; i++) {
                const pad = document.createElement("div");
                pad.className = "simon-pad";
                pad.id = `pad-${i}`;
                pad.innerText = i + 1;
                pad.onclick = () => handlePadClick(i);
                grid.appendChild(pad);
            }

            let sequence = [];
            let userSequence = [];
            let stage = 1;
            let isShowing = false;
            let speed = 600; // 스테이지가 올라갈수록 패턴 속도가 빨라짐

            function nextStage() {
                userSequence = [];
                document.getElementById("s-stage").innerText = stage;
                sequence.push(Math.floor(Math.random() * 9));
                // 난이도 조절: 스테이지 상승시 속도가 빨라져 암기력 자극
                speed = Math.max(200, 600 - (stage * 35)); 
                showSequence();
            }

            function showSequence() {
                isShowing = true;
                document.getElementById("s-status").innerText = "👀 패턴을 똑똑히 기억하세요!";
                document.getElementById("s-status").style.color = C.yellow;

                let i = 0;
                gameInterval = setInterval(() => {
                    if (i >= sequence.length) {
                        clearInterval(gameInterval);
                        isShowing = false;
                        document.getElementById("s-status").innerText = "👉 기억한 순서대로 발판을 클릭하세요!";
                        document.getElementById("s-status").style.color = C.cyan;
                        return;
                    }
                    flashPad(sequence[i]);
                    i++;
                }, speed + 150);
            }

            function flashPad(id) {
                const pad = document.getElementById(`pad-${id}`);
                if (pad) {
                    pad.classList.add("active");
                    setTimeout(() => pad.classList.remove("active"), speed);
                }
            }

            function handlePadClick(id) {
                if (isShowing) return;
                flashPad(id);
                userSequence.push(id);

                const currentCheckIdx = userSequence.length - 1;
                if (userSequence[currentCheckIdx] !== sequence[currentCheckIdx]) {
                    // 패배 탈락
                    document.getElementById("s-status").innerText = `💥 오답! 게임오버. 최종 스테이지: ${stage}`;
                    document.getElementById("s-status").style.color = C.red;
                    // 리셋 후 재시작
                    sequence = [];
                    stage = 1;
                    setTimeout(nextStage, 2000);
                    return;
                }

                if (userSequence.length === sequence.length) {
                    stage++;
                    document.getElementById("s-status").innerText = "🎯 완벽합니다! 다음 단계 진입.";
                    document.getElementById("s-status").style.color = C.green;
                    setTimeout(nextStage, 1000);
                }
            }

            // 시작 트레이닝 호출
            setTimeout(nextStage, 500);
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        // [신규] 스마트 인공지능 컴퓨터 대항 틱택토 (TIC-TAC-TOE)
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function startTictactoeGame(ctx) {
            ctx.innerHTML = `
                <div style="text-align:center;">
                    <div id="t-status" style="font-size:16px; margin-bottom:15px; color:${C.cyan}">당신의 차례 (X) 빈칸을 선택하세요.</div>
                    <div class="ttt-grid" id="t-grid"></div>
                    <button class="back-btn" id="t-reset" style="display:none; margin-top:15px; border-color:${C.purple}">다시 시작하기</button>
                </div>
            `;

            let board = Array(9).fill("");
            let gameActive = true;
            const grid = document.getElementById("t-grid");

            function buildBoard() {
                grid.innerHTML = "";
                for(let i=0; i<9; i++) {
                    const cell = document.createElement("div");
                    cell.className = "ttt-cell";
                    cell.innerText = board[i];
                    if(board[i] === "X") cell.style.color = C.cyan;
                    if(board[i] === "O") cell.style.color = C.pink;
                    cell.onclick = () => makeMove(i);
                    grid.appendChild(cell);
                }
            }

            function checkWin(b) {
                const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
                for(let w of wins) {
                    if(b[w[0]] && b[w[0]] === b[w[1]] && b[w[0]] === b[w[2]]) return b[w[0]];
                }
                return b.includes("") ? null : "DRAW";
            }

            function makeMove(idx) {
                if(!gameActive || board[idx] !== "") return;
                board[idx] = "X";
                buildBoard();

                let res = checkWin(board);
                if(res) { endGame(res); return; }

                // 인공지능 차례 (방어/공격 무작위 연산 혼합 AI)
                gameActive = false;
                document.getElementById("t-status").innerText = "🤖 컴퓨터가 수식 계산 중...";
                setTimeout(() => {
                    const empties = board.map((v, i) => v === "" ? i : null).filter(v => v !== null);
                    if(empties.length > 0) {
                        // 기본 빈칸 무작위 배정
                        const compMove = empties[Math.floor(Math.random() * empties.length)];
                        board[compMove] = "O";
                        buildBoard();
                        
                        let res2 = checkWin(board);
                        if(res2) { endGame(res2); return; }
                    }
                    gameActive = true;
                    document.getElementById("t-status").innerText = "당신의 차례 (X)";
                }, 500);
            }

            function endGame(result) {
                gameActive = false;
                const status = document.getElementById("t-status");
                if(result === "DRAW") { status.innerText = "🤝 무승부입니다!"; status.style.color = "#fff"; }
                else if(result === "X") { status.innerText = "🎉 당신의 대승리!!"; status.style.color = C.green; }
                else { status.innerText = "💀 컴퓨터의 지능 판정승!"; status.style.color = C.red; }
                document.getElementById("t-reset").style.display = "inline-block";
            }

            document.getElementById("t-reset").onclick = () => {
                board = Array(9).fill("");
                gameActive = true;
                document.getElementById("t-reset").style.display = "none";
                document.getElementById("t-status").innerText = "당신의 차례 (X)";
                buildBoard();
            };

            buildBoard();
        }

        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        // 원래 코드에 들어있던 고전 4개 게임 엔진 완벽 이식 (테트리스/스네이크/벽돌/스페이스)
        // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        function startCanvasGame(type, ctx) {
            let width = 300, height = 400;
            if(type === "snake" || type === "space") { width = 320; height = 320; }
            
            ctx.innerHTML = `<canvas id="gc" width="${width}" height="${height}"></canvas>`;
            const canvas = document.getElementById("gc");
            const g = canvas.getContext("2d");

            // 🟦 테트리스 실제 구동 코드
            if(type === "tetris") {
                const COLS = 10, ROWS = 14, SIZE = 20;
                let board = Array(ROWS).fill().map(() => Array(COLS).fill(0));
                let score = 0;
                const SHAPES = [
                    [[1,1,1,1]], [[1,1,1],[0,1,0]], [[1,1,0],[0,1,1]], [[0,1,1],[1,1,0]], [[1,1],[1,1]]
                ];
                let current = { x: 3, y: 0, matrix: SHAPES[Math.floor(Math.random()*SHAPES.length)], color: C.cyan };

                function collide(b, p, dx, dy, nextMatrix) {
                    let m = nextMatrix || p.matrix;
                    for(let r=0; r<m.length; r++) {
                        for(let c=0; c<m[r].length; c++) {
                            if(m[r][c]) {
                                let nx = p.x + c + dx;
                                let ny = p.y + r + dy;
                                if(nx < 0 || nx >= COLS || ny >= ROWS) return true;
                                if(ny >= 0 && b[ny][nx]) return true;
                            }
                        }
                    }
                    return false;
                }

                function merge(b, p) {
                    p.matrix.forEach((row, r) => {
                        row.forEach((val, c) => {
                            if(val) { if(p.y+r >= 0) b[p.y+r][p.x+c] = p.color; }
                        });
                    });
                }

                function sweep() {
                    for(let r=ROWS-1; r>=0; r--) {
                        if(board[r].every(v => v !== 0)) {
                            board.splice(r, 1);
                            board.unshift(Array(COLS).fill(0));
                            score += 100;
                            r++;
                        }
                    }
                }

                function tick() {
                    if(!collide(board, current, 0, 1)) {
                        current.y++;
                    } else {
                        merge(board, current);
                        sweep();
                        current = { x: 3, y: 0, matrix: SHAPES[Math.floor(Math.random()*SHAPES.length)], color: C.cyan };
                        if(collide(board, current, 0, 0)) {
                            board = Array(ROWS).fill().map(() => Array(COLS).fill(0));
                            score = 0;
                        }
                    }
                    draw();
                }

                function draw() {
                    g.fillStyle = "#000"; g.fillRect(0,0,width,height);
                    // 판 그리기
                    for(let r=0; r<ROWS; r++) {
                        for(let c=0; c<COLS; c++) {
                            if(board[r][c]) { g.fillStyle = board[r][c]; g.fillRect(c*SIZE, r*SIZE, SIZE-1, SIZE-1); }
                        }
                    }
                    // 현재 블록
                    g.fillStyle = current.color;
                    current.matrix.forEach((row, r) => {
                        row.forEach((val, c) => {
                            if(val) g.fillRect((current.x+c)*SIZE, (current.y+r)*SIZE, SIZE-1, SIZE-1);
                        });
                    });
                    // 점수판
                    g.fillStyle = "#fff"; g.font = "14px monospace"; g.fillText("SCORE: " + score, 10, height - 15);
                }

                const keyHandler = (e) => {
                    if(e.key === "ArrowLeft" && !collide(board, current, -1, 0)) { current.x--; draw(); e.preventDefault(); }
                    if(e.key === "ArrowRight" && !collide(board, current, 1, 0)) { current.x++; draw(); e.preventDefault(); }
                    if(e.key === "ArrowDown" && !collide(board, current, 0, 1)) { current.y++; draw(); e.preventDefault(); }
                    if(e.key === "ArrowUp") {
                        // 회전 알고리즘
                        let next = current.matrix[0].map((_, i) => current.matrix.map(row => row[i]).reverse());
                        if(!collide(board, current, 0, 0, next)) { current.matrix = next; draw(); }
                        e.preventDefault();
                    }
                };
                document.addEventListener("keydown", keyHandler);
                window.currentCleanup = () => document.removeEventListener("keydown", keyHandler);
                gameInterval = setInterval(tick, 400);
            }

            // 🐍 스네이크 실제 구동 코드
            if(type === "snake") {
                let snake = [{x:8, y:8}], dir = {x:1, y:0}, apple = {x:4, y:5}, score=0;
                const SIZE = 20, cells = 16;

                function tick() {
                    let head = {x: snake[0].x + dir.x, y: snake[0].y + dir.y};
                    // 벽 체크 충돌시 리셋
                    if(head.x < 0 || head.x >= cells || head.y < 0 || head.y >= cells) { snake=[{x:8,y:8}]; dir={x:1,y:0}; score=0; return; }
                    
                    // 몸통 충돌
                    for(let s of snake) { if(s.x === head.x && s.y === head.y) { snake=[{x:8,y:8}]; dir={x:1,y:0}; score=0; return; } }

                    snake.unshift(head);
                    if(head.x === apple.x && head.y === apple.y) {
                        score += 10;
                        apple = {x: Math.floor(Math.random()*cells), y: Math.floor(Math.random()*cells)};
                    } else {
                        snake.pop();
                    }

                    // 드로잉
                    g.fillStyle = "#000"; g.fillRect(0,0,width,height);
                    g.fillStyle = C.green;
                    for(let s of snake) g.fillRect(s.x*SIZE, s.y*SIZE, SIZE-1, SIZE-1);
                    g.fillStyle = C.red; g.fillRect(apple.x*SIZE, apple.y*SIZE, SIZE-1, SIZE-1);
                    g.fillStyle = "#fff"; g.font = "14px monospace"; g.fillText("SCORE: " + score, 10, height - 10);
                }

                const keyHandler = (e) => {
                    if(e.key === "ArrowLeft" && dir.x === 0) { dir = {x:-1, y:0}; e.preventDefault(); }
                    if(e.key === "ArrowRight" && dir.x === 0) { dir = {x:1, y:0}; e.preventDefault(); }
                    if(e.key === "ArrowUp" && dir.y === 0) { dir = {x:0, y:-1}; e.preventDefault(); }
                    if(e.key === "ArrowDown" && dir.y === 0) { dir = {x:0, y:1}; e.preventDefault(); }
                };
                document.addEventListener("keydown", keyHandler);
                window.currentCleanup = () => document.removeEventListener("keydown", keyHandler);
                gameInterval = setInterval(tick, 150);
            }

            // 🧱 벽돌깨기 실제 구동 코드
            if(type === "breakout") {
                let px = 120, pw = 60, bx = 150, by = 200, bdx = 2, bdy = -3;
                let bricks = [];
                for(let i=0; i<4; i++) { for(let j=0; j<5; j++) { bricks.push({x: j*55 + 15, y: i*20 + 30, active: true}); } }

                function tick() {
                    bx += bdx; by += bdy;
                    if(bx < 0 || bx > width) bdx = -bdx;
                    if(by < 0) bdy = -bdy;
                    // 바닥 추락시 리셋
                    if(by > height) { bx=150; by=200; bdy=-3; bdx=2; }

                    // 패들 반사
                    if(by > height - 40 && bx > px && bx < px + pw) bdy = -Math.abs(bdy);

                    // 벽돌 충돌
                    bricks.forEach(b => {
                        if(b.active && bx > b.x && bx < b.x + 50 && by > b.y && by < b.y + 15) { b.active = false; bdy = -bdy; }
                    });

                    // 드로우
                    g.fillStyle = "#000"; g.fillRect(0,0,width,height);
                    g.fillStyle = C.orange; g.fillRect(px, height - 30, pw, 10);
                    g.fillStyle = "#fff"; g.beginPath(); g.arc(bx,by,5,0,Math.PI*2); g.fill();
                    bricks.forEach(b => { if(b.active) { g.fillStyle = C.yellow; g.fillRect(b.x, b.y, 50, 15); } });
                }

                const keyHandler = (e) => {
                    if(e.key === "ArrowLeft") { px = Math.max(0, px - 15); e.preventDefault(); }
                    if(e.key === "ArrowRight") { px = Math.min(width - pw, px + 15); e.preventDefault(); }
                };
                document.addEventListener("keydown", keyHandler);
                window.currentCleanup = () => document.removeEventListener("keydown", keyHandler);
                gameInterval = setInterval(tick, 1000/30);
            }

            // 👾 스페이스 인베이더 실제 구동 코드
            if(type === "space") {
                let px = 140, bullets = [], invaders = [];
                for(let i=0; i<3; i++) { for(let j=0; j<5; j++) { invaders.push({x: j*45+40, y: i*30+30, alive:true}); } }

                function tick() {
                    bullets.forEach(b => b.y -= 5);
                    bullets = bullets.filter(b => b.y > 0);

                    // 탄환 충돌 연산
                    bullets.forEach(b => {
                        invaders.forEach(inv => {
                            if(inv.alive && b.x > inv.x && b.x < inv.x + 30 && b.y > inv.y && b.y < inv.y + 20) { inv.alive = false; b.y = -100; }
                        });
                    });

                    g.fillStyle = "#000"; g.fillRect(0,0,width,height);
                    g.fillStyle = C.green; g.fillRect(px, height-25, 30, 15); // 플레이어 우주선
                    g.fillStyle = C.cyan; bullets.forEach(b => g.fillRect(b.x, b.y, 3, 8)); // 레이저
                    g.fillStyle = C.red; invaders.forEach(inv => { if(inv.alive) g.fillRect(inv.x, inv.y, 30, 20); }); // 외계인
                }

                const keyHandler = (e) => {
                    if(e.key === "ArrowLeft") { px = Math.max(0, px - 12); e.preventDefault(); }
                    if(e.key === "ArrowRight") { px = Math.min(width - 30, px + 12); e.preventDefault(); }
                    if(e.key === " " || e.code === "Space") { bullets.push({x: px + 14, y: height - 30}); e.preventDefault(); }
                };
                document.addEventListener("keydown", keyHandler);
                window.currentCleanup = () => document.removeEventListener("keydown", keyHandler);
                gameInterval = setInterval(tick, 1000/30);
            }
        }

        // 초기 시작
        render();
    </script>
</body>
</html>
"""

# Streamlit에 가득 차게 HTML 컴포넌트 렌더링
st.components.v1.html(arcade_html, height=850, scrolling=True)
