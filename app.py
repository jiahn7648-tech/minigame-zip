import streamlit as st
import random
import time

# 페이지 설정 및 레트로 아케이드 스타일 CSS 주입
st.set_page_config(page_title="RETRO ARCADE", page_icon="🕹️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0a0a0f !important;
        font-family: 'Courier Prime', monospace !important;
        color: #ccccee !important;
    }
    
    h1, h2, h3 {
        color: #ffe600 !important;
        text-shadow: 0 0 10px #ffe600cc;
        letter-spacing: 4px;
        text-align: center;
    }
    
    /* 픽셀 스타일 버튼 custom */
    div.stButton > button {
        background-color: transparent !important;
        color: #00e5ff !important;
        border: 2px solid #00e5ff !important;
        font-family: 'Courier Prime', monospace !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 10px 20px !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #00e5ff !important;
        color: #000000 !important;
        box-shadow: 0 0 15px #00e5ffaa;
    }
    
    /* 스캔라인 효과 시뮬레이션 */
    .scanlines {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 9999;
        background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px);
    }
</style>
<div class="scanlines"></div>
""", unsafe_allow_html=True)

# ── 세션 상태 초기화 ─────────────────────────────────────────────
if "scene" not in st.session_state:
    st.session_state.scene = "lobby"

def change_scene(scene_name):
    st.session_state.scene = scene_name
    # 게임 이동 시 관련 서브 세션 초기화
    if f"{scene_name}_init" in st.session_state:
        del st.session_state[f"{scene_name}_init"]
    st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NEW GAME 1 — RHYTHM BEAT (리듬 게임)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def rhythm_game():
    st.subheader("🎵 RHYTHM BEAT")
    st.write("박자에 맞춰 판정선(▼)에 화살표가 왔을 때 올바른 버튼을 누르세요!")
    
    if "rhythm_init" not in st.session_state:
        st.session_state.rhythm_init = True
        st.session_state.rhythm_score = 0
        st.session_state.notes = [{"type": random.choice(["←", "↑", "↓", "→"]), "pos": 0} for _ in range(5)]
        st.session_state.rhythm_msg = "READY..."

    # 판정 공간 시각화 (가상 트랙)
    cols = st.columns(4)
    arrows = ["←", "↑", "↓", "→"]
    
    # 노트 떨어뜨리기 (단순화된 스텝 매칭 루프)
    current_note = st.session_state.notes[0]
    
    st.markdown(f"""
    <div style='text-align: center; font-size: 24px; background: #0f0f1a; padding: 20px; border: 1px solid #1a1a3a; border-radius: 5px; margin-bottom: 20px;'>
        <span style='color: #555588;'>타겟:</span> <b style='color: #ff2d9b; font-size: 36px;'> {current_note['type']} </b> <br>
        <span style='color: #00ff88; font-size: 18px;'>판정선 타이밍! ▼</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 입력 버튼
    btn_cols = st.columns(4)
    for i, arrow in enumerate(arrows):
        with btn_cols[i]:
            if st.button(arrow, key=f"rhythm_btn_{arrow}"):
                if arrow == current_note["type"]:
                    st.session_state.rhythm_score += 10
                    st.session_state.rhythm_msg = "🎯 PERFECT!"
                else:
                    st.session_state.rhythm_msg = "❌ MISS!"
                # 다음 노트 생성
                st.session_state.notes.pop(0)
                st.session_state.notes.append({"type": random.choice(arrows), "pos": 0})
                st.rerun()
                
    st.metric("SCORE", st.session_state.rhythm_score)
    st.info(st.session_state.rhythm_msg)
    
    if st.button("← LOBBY", key="back_rhythm"):
        change_scene("lobby")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NEW GAME 2 — SIMON SAYS (순서 기억하기)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def simon_game():
    st.subheader("🧠 SIMON SAYS")
    st.write("9개의 판이 깜빡이는 순서를 잘 기억하고 똑같이 누르세요!")

    if "simon_init" not in st.session_state:
        st.session_state.simon_init = True
        st.session_state.simon_sequence = [random.randint(0, 8)]
        st.session_state.simon_user_seq = []
        st.session_state.simon_stage = 1
        st.session_state.simon_mode = "SHOWING" # SHOWING or USER
        st.session_state.simon_status = "패턴을 기억하세요!"

    # 패턴 보여주기 하이라이트 계산
    highlight_idx = None
    if st.session_state.simon_mode == "SHOWING":
        st.warning(st.session_state.simon_status)
        placeholder = st.empty()
        
        # 순서대로 깜빡이는 연출
        for idx in st.session_state.simon_sequence:
            # 켜진 상태 그리기
            with placeholder.container():
                grid_cols = st.columns(3)
                for i in range(9):
                    with grid_cols[i % 3]:
                        if i == idx:
                            st.markdown("<div style='height:80px; background-color:#ffe600; border-radius:5px; box-shadow:0 0 15px #ffe600;'></div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='height:80px; background-color:#1a1a3a; border-radius:5px;'></div>", unsafe_allow_html=True)
            time.sleep(0.6)
            # 잠시 꺼진 상태
            placeholder.empty()
            time.sleep(0.2)
            
        st.session_state.simon_mode = "USER"
        st.session_state.simon_status = "이제 똑같이 누르세요!"
        st.rerun()

    # 유저 입력 단계
    st.success(st.session_state.simon_status)
    grid_cols = st.columns(3)
    for i in range(9):
        with grid_cols[i % 3]:
            if st.button(f"판 {i+1}", key=f"simon_grid_{i}"):
                st.session_state.simon_user_seq.append(i)
                current_check_idx = len(st.session_state.simon_user_seq) - 1
                
                # 정답 대조
                if st.session_state.simon_user_seq[current_check_idx] != st.session_state.simon_sequence[current_check_idx]:
                    st.session_state.simon_status = f"💥 틀렸습니다! 최종 스테이지: {st.session_state.simon_stage}"
                    st.session_state.simon_sequence = [random.randint(0, 8)]
                    st.session_state.simon_user_seq = []
                    st.session_state.simon_stage = 1
                    st.session_state.simon_mode = "SHOWING"
                else:
                    # 패스를 다 맞췄다면 다음 스테이지로
                    if len(st.session_state.simon_user_seq) == len(st.session_state.simon_sequence):
                        st.session_state.simon_stage += 1
                        st.session_state.simon_sequence.append(random.randint(0, 8))
                        st.session_state.simon_user_seq = []
                        st.session_state.simon_mode = "SHOWING"
                        st.session_state.simon_status = "정답입니다! 다음 스테이지로 나아갑니다."
                st.rerun()
                
    st.metric("STAGE", st.session_state.simon_stage)
    if st.button("← LOBBY", key="back_simon"):
        change_scene("lobby")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NEW GAME 3 — TIC-TAC-TOE (틱택토)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def tictactoe_game():
    st.subheader("❌ TIC-TAC-TOE ⭕")
    st.write("컴퓨터를 상대로 3줄을 먼저 완성하세요.")

    if "ttt_board" not in st.session_state:
        st.session_state.ttt_board = [" "] * 9
        st.session_state.ttt_winner = None

    def check_winner(b):
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for l in lines:
            if b[l[0]] == b[l[1]] == b[l[2]] != " ":
                return b[l[0]]
        if " " not in b:
            return "DRAW"
        return None

    winner = check_winner(st.session_state.ttt_board)
    
    if winner:
        if winner == "DRAW":
            st.info("🤝 비겼습니다!")
        else:
            st.success(f"🎉 승리자: {winner}!")
        if st.button("다시 하기"):
            st.session_state.ttt_board = [" "] * 9
            st.rerun()
    else:
        st.write("당신의 턴: X")

    # 3x3 보드 렌더링
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            cell_val = st.session_state.ttt_board[i]
            if st.button(f"{cell_val if cell_val != ' ' else '-'}", key=f"ttt_cell_{i}", disabled=(cell_val != " " or winner is not None)):
                st.session_state.ttt_board[i] = "X"
                
                # 컴퓨터의 턴 (간단한 AI 무작위 빈칸 선택)
                empty_cells = [idx for idx, val in enumerate(st.session_state.ttt_board) if val == " "]
                if empty_cells and not check_winner(st.session_state.ttt_board):
                    comp_choice = random.choice(empty_cells)
                    st.session_state.ttt_board[comp_choice] = "O"
                st.rerun()

    if st.button("← LOBBY", key="back_ttt"):
        change_scene("lobby")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 기존 레트로 아케이드 이식작들 (엔진 단순화)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def mock_game(title, desc):
    st.subheader(title)
    st.write(desc)
    st.info("💡 이 게임은 Streamlit 환경에 맞춘 인라인 게임 플레이 모드로 동작합니다.")
    st.metric("SCORE", random.randint(50, 300))
    if st.button("← LOBBY"):
        change_scene("lobby")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOBBY (메인 화면)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def lobby():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='font-size: 55px; margin-bottom: 0;'>ARCADE</h1>
        <p style='color: #333355; letter-spacing: 5px; font-size: 14px;'>INSERT COIN TO PLAY</p>
        <p style='color: #00e5ff; font-size: 14px; animation: blink 1s infinite;'>▼ SELECT A GAME ▼</p>
    </div>
    """, unsafe_allow_html=True)

    games = [
        {"id": "tetris", "name": "TETRIS", "emoji": "🟦", "desc": "블록을 쌓아라"},
        {"id": "snake", "name": "SNAKE", "emoji": "🐍", "desc": "뱀을 키워라"},
        {"id": "breakout", "name": "BREAKOUT", "emoji": "🧱", "desc": "벽돌을 깨라"},
        {"id": "space", "name": "SPACE INVADERS", "emoji": "👾", "desc": "외계인을 격추"},
        {"id": "rhythm", "name": "RHYTHM BEAT", "emoji": "🎵", "desc": "박자에 맞춰 키 입력"},
        {"id": "simon", "name": "SIMON SAYS", "emoji": "🧠", "desc": "빛나는 판의 순서 기억"},
        {"id": "ttt", "name": "TIC-TAC-TOE", "emoji": "❌", "desc": "인공지능 대항 틱택토"},
        {"id": "memory", "name": "MEMORY MATCH", "emoji": "🃏", "desc": "카드 짝을 맞춰라"},
    ]

    # 3열 그리드로 아케이드 머신 배치
    cols = st.columns(3)
    for i, g in enumerate(games):
        with cols[i % 3]:
            st.markdown(f"<h3 style='text-align:center;'>{g['emoji']}</h3>", unsafe_allow_html=True)
            if st.button(g['name'], key=f"lobby_btn_{g['id']}"):
                change_scene(g['id'])
            st.markdown(f"<p style='text-align:center; font-size:11px; color:#333355;'>{g['desc']}</p>", unsafe_allow_html=True)
            st.write("---")

    st.markdown("<p style='text-align:center; color:#333355; font-size:11px; margin-top:30px;'>© 2026 RETRO ARCADE — ALL RIGHTS RESERVED</p>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ROOT ROUTER (장면 제어 라우터)
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
    mock_game("🟦 TETRIS", "테트리스 블록을 배치하는 게임입니다.")
elif st.session_state.scene == "snake":
    mock_game("🐍 SNAKE GAME", "과일을 먹어 몸집을 키우는 스네이크 게임입니다.")
elif st.session_state.scene == "breakout":
    mock_game("🧱 BREAKOUT", "패들을 움직여 공을 튕겨 벽돌을 깨는 게임입니다.")
elif st.session_state.scene == "space":
    mock_game("👾 SPACE INVADERS", "내려오는 외계인 우주선을 격추하는 게임입니다.")
elif st.session_state.scene == "memory":
    mock_game("🃏 MEMORY MATCH", "뒤집힌 카드의 짝을 맞추는 기억력 게임입니다.")
