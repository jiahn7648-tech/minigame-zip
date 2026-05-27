import streamlit as st
import random
import time

# 페이지 기본 설정 및 원래 코드의 딥다크 네온 테마 적용
st.set_page_config(page_title="RETRO ARCADE", page_icon="🕹️", layout="centered")

# 원래 코드의 컬러 시스템 정의
C_BG = "#0a0a0f"
C_PANEL = "#0f0f1a"
C_BORDER = "#1a1a3a"
C_TEXT = "#ccccee"
C_DIM = "#333355"

# 원래 코드의 감성을 완벽히 구현하기 위한 오리지널 CSS 스타일링
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {C_BG} !important;
        font-family: 'Courier New', 'Lucida Console', monospace !important;
        color: {C_TEXT} !important;
    }}
    
    /* 오리지널 타이틀 스타일 */
    .arcade-title {{
        font-family: 'Courier New', 'Lucida Console', monospace;
        font-size: 50px;
        font-weight: bold;
        color: #ffe600;
        text-shadow: 0 0 10px rgba(255, 230, 0, 0.8);
        letter-spacing: 4px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 0px;
    }}
    
    .arcade-subtitle {{
        font-family: 'Courier New', 'Lucida Console', monospace;
        color: {C_DIM};
        letter-spacing: 5px;
        font-size: 11px;
        text-align: center;
        margin-bottom: 40px;
    }}

    /* 원래 코드의 카드 슬롯 스타일 재현 */
    .game-card {{
        background: {C_PANEL};
        border: 2px solid {C_BORDER};
        border-radius: 8px;
        padding: 24px;
        text-align: center;
        transition: all 0.2s ease;
        margin-bottom: 20px;
        min-height: 180px;
    }}
    
    /* 안내 박스 스타일 */
    .info-box {{
        background-color: {C_PANEL};
        border-left: 4px solid #00e5ff;
        padding: 15px;
        margin-bottom: 25px;
        border-radius: 4px;
    }}
    
    /* 텍스트 가독성 확보를 위한 강제 색상 지정 */
    p, span, label {{
        color: {C_TEXT} !important;
    }}
    
    /* 스캔라인 레이어 */
    .scanlines {{
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 9999;
        background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.13) 2px, rgba(0,0,0,0.13) 4px);
    }}
</style>
<div class="scanlines"></div>
""", unsafe_allow_html=True)

# ── 세션 상태 관리 ─────────────────────────────────────────────
if "scene" not in st.session_state:
    st.session_state.scene = "lobby"

def change_scene(scene_name):
    st.session_state.scene = scene_name
    if f"{scene_name}_init" in st.session_state:
        del st.session_state[f"{scene_name}_init"]
    st.rerun()

# ── 각 게임 화면 상단에 띄워줄 안내 가이드 출력 함수 ─────────────────────
def render_game_guide(title, color, description, controls):
    st.markdown(f"""
    <div class="info-box" style="border-left-color: {color};">
        <h2 style="color: {color}; margin-top:0; font-size:24px;">🎮 {title}</h2>
        <p style="margin: 5px 0;"><b>📝 게임 설명:</b> {description}</p>
        <p style="margin: 5px 0; color: #ff2d9b !important;"><b>🕹️ 조작 방법:</b> {controls}</p>
    </div>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GAME 1 — RHYTHM BEAT (리듬 게임)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def rhythm_game():
    render_game_guide(
        title="RHYTHM BEAT", 
        color="#ff2d9b", 
        description="위에서 아래로 떨어지는 비트 화살표를 보고 타겟 판정선에 맞춰 정확한 키를 입력하세요.",
        controls="화면에 표시되는 방향키 버튼(←, ↑, ↓, →)을 타이밍에 맞춰 마우스로 클릭합니다."
    )
    
    if "rhythm_init" not in st.session_state:
        st.session_state.rhythm_init = True
        st.session_state.rhythm_score = 0
        st.session_state.notes = [{"type": random.choice(["←", "↑", "↓", "→"])} for _ in range(5)]
        st.session_state.rhythm_msg = "READY..."

    current_note = st.session_state.notes[0]
    
    st.markdown(f"""
    <div style='text-align: center; background: {C_PANEL}; padding: 30px; border: 2px solid {C_BORDER}; border-radius: 8px; margin-bottom: 20px;'>
        <div style='color: {C_DIM}; font-size: 14px; letter-spacing: 2px;'>TARGET NOTE</div>
        <div style='color: #ff2d9b; font-size: 60px; font-weight: bold; margin: 10px 0;'>{current_note['type']}</div>
        <div style='color: #00ff88; font-size: 14px;'>▼ NOW HIT THE BUTTON ▼</div>
    </div>
    """, unsafe_allow_html=True)
    
    arrows = ["←", "↑", "↓", "→"]
    btn_cols = st.columns(4)
    for i, arrow in enumerate(arrows):
        with btn_cols[i]:
            if st.button(arrow, key=f"rhythm_btn_{arrow}", use_container_width=True):
                if arrow == current_note["type"]:
                    st.session_state.rhythm_score += 10
                    st.session_state.rhythm_msg = "🎯 PERFECT!"
                else:
                    st.session_state.rhythm_msg = "❌ MISS!"
                st.session_state.notes.pop(0)
                st.session_state.notes.append({"type": random.choice(arrows)})
                st.rerun()
                
    st.metric("SCORE", st.session_state.rhythm_score)
    st.write(f"판정 피드백: **{st.session_state.rhythm_msg}**")
    
    if st.button("◀ BACK TO LOBBY", key="back_rhythm"):
        change_scene("lobby")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GAME 2 — SIMON SAYS (순서 기억력 게임)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def simon_game():
    render_game_guide(
        title="SIMON SAYS", 
        color="#ffe600", 
        description="9개의 발판이 차례대로 번쩍이며 무작위 패턴을 생성합니다. 암기가 끝나면 제시된 순서대로 정확히 발판을 눌러야 합니다.",
        controls="마우스를 사용하여 시스템이 보여준 순서대로 1번부터 9번까지의 발판을 순서대로 누르세요. 단계가 올라갈수록 기억할 길이가 늘어납니다."
    )

    if "simon_init" not in st.session_state:
        st.session_state.simon_init = True
        st.session_state.simon_sequence = [random.randint(0, 8)]
        st.session_state.simon_user_seq = []
        st.session_state.simon_stage = 1
        st.session_state.simon_mode = "SHOWING"
        st.session_state.simon_status = "컴퓨터의 패턴을 암기하는 중입니다..."

    # 패턴 재생 상태 처리
    if st.session_state.simon_mode == "SHOWING":
        st.info(st.session_state.simon_status)
        placeholder = st.empty()
        
        for idx in st.session_state.simon_sequence:
            with placeholder.container():
                grid_cols = st.columns(3)
                for i in range(9):
                    with grid_cols[i % 3]:
                        if i == idx:
                            st.markdown("<div style='height:70px; background-color:#ffe600; border-radius:4px; box-shadow:0 0 15px #ffe600;'></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='height:70px; background-color:{C_PANEL}; border:1px solid {C_BORDER}; border-radius:4px;'></div>", unsafe_allow_html=True)
            time.sleep(0.6)
            placeholder.empty()
            time.sleep(0.15)
            
        st.session_state.simon_mode = "USER"
        st.session_state.simon_status = "기억한 순서대로 버튼을 클릭하세요!"
        st.rerun()

    # 플레이어 입력 입력 대기 상태
    st.success(st.session_state.simon_status)
    grid_cols = st.columns(3)
    for i in range(9):
        with grid_cols[i % 3]:
            if st.button(f"PAD {i+1}", key=f"simon_grid_{i}", use_container_width=True):
                st.session_state.simon_user_seq.append(i)
                curr_idx = len(st.session_state.simon_user_seq) - 1
                
                if st.session_state.simon_user_seq[curr_idx] != st.session_state.simon_sequence[curr_idx]:
                    st.error(f"💥 패턴이 틀렸습니다! 최종 기록: {st.session_state.simon_stage} 스테이지")
                    st.session_state.simon_sequence = [random.randint(0, 8)]
                    st.session_state.simon_user_seq = []
                    st.session_state.simon_stage = 1
                    st.session_state.simon_mode = "SHOWING"
                else:
                    if len(st.session_state.simon_user_seq) == len(st.session_state.simon_sequence):
                        st.session_state.simon_stage += 1
                        st.session_state.simon_sequence.append(random.randint(0, 8))
                        st.session_state.simon_user_seq = []
                        st.session_state.simon_mode = "SHOWING"
                        st.session_state.simon_status = "정답입니다! 패턴이 한 단계 더 어려워집니다."
                st.rerun()
                
    st.metric("STAGE LEVEL", st.session_state.simon_stage)
    if st.button("◀ BACK TO LOBBY", key="back_simon"):
        change_scene("lobby")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GAME 3 — TIC-TAC-TOE (틱택토)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def tictactoe_game():
    render_game_guide(
        title="TIC-TAC-TOE", 
        color="#00e5ff", 
        description="가로, 세로, 대각선 중 한 줄에 먼저 자신의 표식을 3개 연속으로 놓는 클래식 보드 게임입니다. 플레이어는 X, 인공지능 컴퓨터는 O입니다.",
        controls="3x3 그리드 보드 위의 빈 격자판을 마우스로 클릭하여 본인의 돌(X)을 배치하세요."
    )

    if "ttt_board" not in st.session_state:
        st.session_state.ttt_board = [" "] * 9

    def check_winner(b):
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for l in lines:
            if b[l[0]] == b[l[1]] == b[l[2]] != " ": return b[l[0]]
        return "DRAW" if " " not in b else None

    winner = check_winner(st.session_state.ttt_board)
    
    if winner:
        if winner == "DRAW": st.info("🤝 무승부입니다! 박빙의 승부였네요.")
        else: st.success(f"🎉 승리자 판정: {winner}의 승리!")
        if st.button("보드 초기화 후 다시 하기", use_container_width=True):
            st.session_state.ttt_board = [" "] * 9
            st.rerun()

    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            cell_val = st.session_state.ttt_board[i]
            # 비어있을 때는 하이픈(-) 처리하여 직관성 확보
            display_text = cell_val if cell_val != " " else "-"
            if st.button(display_text, key=f"ttt_cell_{i}", disabled=(cell_val != " " or winner is not None), use_container_width=True):
                st.session_state.ttt_board[i] = "X"
                
                # 빈 공간 무작위 연산 기반의 컴 턴 처리
                empties = [idx for idx, val in enumerate(st.session_state.ttt_board) if val == " "]
                if empties and not check_winner(st.session_state.ttt_board):
                    st.session_state.ttt_board[random.choice(empties)] = "O"
                st.rerun()

    if st.button("◀ BACK TO LOBBY", key="back_ttt"):
        change_scene("lobby")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 기존 아케이드 서브 게임 구조체 (가이드 이식 완료)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def original_mock_game(title, color, desc, controls):
    render_game_guide(title=title, color=color, description=desc, controls=controls)
    st.markdown(f"""
    <div style='text-align: center; background: {C_PANEL}; border:1px dashed {C_BORDER}; padding: 40px; margin-bottom: 20px;'>
        <p style='color: {color}; font-size:18px;'>⚙️ 해당 오리지널 아케이드 코드를 Streamlit 데이터 모델로 마이그레이션 중입니다.</p>
        <p style='color: {C_TEXT}; font-size:13px;'>실제 구동 인스턴스는 로컬 데스크톱 엔진 빌드 버전을 참고해 주세요.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("◀ BACK TO LOBBY"):
        change_scene("lobby")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOBBY MAIN SCREEN (원래 코드 오리지널 그리드 레이아웃 완전 이식)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def lobby():
    # 상단 헤더 타이틀 복원
    st.markdown('<div class="arcade-title">RETRO ARCADE</div>', unsafe_allow_html=True)
    st.markdown('<div class="arcade-subtitle">6 MINI GAMES (Python Streamlit Edition)</div>', unsafe_allow_html=True)

    # 원래 코드(arcade.jsx)에 선언된 순서 및 메타데이터 복제 (두더지 빠진 자리에 신규 게임 대입)
    games = [
        {"id": "tetris", "name": "TETRIS", "emoji": "🟦", "color": "#00e5ff", "desc": "Falling block puzzle game", "ctrl": "방향키(이동/회전), Spacebar(하드 드롭)"},
        {"id": "snake", "name": "SNAKE", "emoji": "🐍", "color": "#00ff88", "desc": "Classic nibble retro game", "ctrl": "방향키(←, ↑, ↓, →)를 사용하여 방향 전환"},
        {"id": "breakout", "name": "BREAKOUT", "emoji": "🧱", "color": "#ff6d00", "desc": "Brick breaking action", "ctrl": "방향키 좌우(←, →)를 사용해 패들 이동"},
        {"id": "space", "name": "SPACE INVADERS", "emoji": "👾", "color": "#ff1744", "desc": "Retro space shooter arcade", "ctrl": "방향키 좌우로 이동, Spacebar로 미사일 발사"},
        {"id": "rhythm", "name": "RHYTHM BEAT", "emoji": "🎵", "color": "#ff2d9b", "desc": "Timing & key sync music game", "ctrl": "화면 하단의 화살표 버튼 매칭 클릭"},
        {"id": "simon", "name": "SIMON SAYS", "emoji": "🧠", "color": "#ffe600", "desc": "9-Grid pattern memory test", "ctrl": "깜빡인 9개 패드를 똑같은 순서대로 클릭"},
        {"id": "ttt", "name": "TIC-TAC-TOE", "emoji": "❌", "color": "#d500f9", "desc": "Classic match-3 grid board", "ctrl": "3x3 보드판 빈곳을 마우스로 선택"},
        {"id": "memory", "name": "MEMORY MATCH", "emoji": "🃏", "color": "#ccccee", "desc": "Flip cards to find pairs", "ctrl": "카드 뒷면을 마우스로 클릭하여 매칭"},
    ]

    # 원래 코드와 동일한 촘촘한 형태의 반응형 그리드 배열 구현
    cols = st.columns(2)  # 정돈된 2열 형태 구성
    for i, g in enumerate(games):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="game-card" style="border-color: {C_BORDER};">
                <div style="font-size: 36px; margin-bottom: 10px;">{g['emoji']}</div>
                <div style="font-size: 15px; font-weight: bold; color: {g['color']}; letter-spacing: 2px; margin-bottom: 6px;">{g['name']}</div>
                <div style="font-size: 11px; color: {C_TEXT}; opacity: 0.8; margin-bottom: 15px;">{g['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            # 카드의 레이아웃 바로 하단에 정렬된 스타일의 시작 버튼 제공
            if st.button(f"PLAY {g['name']}", key=f"btn_{g['id']}", use_container_width=True):
                change_scene(g['id'])
            st.markdown("<br>", unsafe_allow_html=True)

    # 하단 카피라이트 
    st.markdown(f'<div style="font-family:\'Courier New\'; font-size: 10px; color: {C_DIM}; text-align: center; margin-top: 40px; letter-spacing: 3px;">© 2026 RETRO ARCADE — ALL RIGHTS RESERVED</div>', unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CENTRAL ROUTER (장면 라우터 시스템)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if st.session_state.scene == "lobby":
    lobby()
elif st.session_state.scene == "rhythm":
    rhythm_game()
elif st.session_state.scene == "simon":
    simon_game()
elif st.session_state.scene == "ttt":
    tictactoe_game()
elif st.session_state.scene == "tetris":
    original_mock_game("TETRIS", "#00e5ff", "블록을 한 줄 가득 채워 터뜨리는 고전 테트리스 게임입니다.", "방향키(이동 및 회전), Spacebar(하드드롭)")
elif st.session_state.scene == "snake":
    original_mock_game("SNAKE GAME", "#00ff88", "화면 안의 사과를 먹을 때마다 꼬리가 길어지는 스네이크 게임입니다.", "방향키(←, ↑, ↓, →)를 눌러서 머리 방향 전환")
elif st.session_state.scene == "breakout":
    original_mock_game("BREAKOUT", "#ff6d00", "튕겨 나가는 공을 패들로 받아내 모든 벽돌을 부수는 벽돌깨기 게임입니다.", "좌우 방향키(←, →)를 눌러 바를 좌우로 조작")
elif st.session_state.scene == "space":
    original_mock_game("SPACE INVADERS", "#ff1744", "점점 다가오는 우주 외계인 군단을 레이저포로 방어하는 아케이드 슈팅 슈터 게임입니다.", "좌우 방향키로 이동하며, Spacebar를 눌러 발사")
elif st.session_state.scene == "memory":
    original_mock_game("MEMORY MATCH", "#ccccee", "뒤집힌 카드 더미 속에서 똑같은 짝의 일러스트를 찾는 기억력 매칭 카드 게임입니다.", "마우스 왼쪽 버튼으로 원하는 카드 2장을 순서대로 뒤집기")
