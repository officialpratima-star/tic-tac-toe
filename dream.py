import streamlit as st
import random

# ------------------------------
# Initialization (session state)
# ------------------------------
def init_state():
    defaults = {
        "username": "",
        "page": "login",          # login, home, vs_cpu, vs_multi, shop, result
        "coins": 0,
        "board": [["" for _ in range(3)] for _ in range(3)],
        "turn": "X",              # turn holder for current game
        "game_over": False,
        "winner": None,           # "X" / "O" / "Tie" / None
        "mode": None,             # "cpu" or "multi"
        # Owned items in shop
        "owned_symbols": {"classic"}, # classic is free
        "owned_backgrounds": {"plain"},
        # Selected skins
        "symbol_skin": "classic",     # classic | emoji | sci | fun
        "background_skin": "plain",   # plain | pastel | dark | grid
        # Player display names for multiplayer
        "p1_name": "Player X",
        "p2_name": "Player O",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ------------------------------
# Skins (symbols + backgrounds)
# ------------------------------
SYMBOL_SETS = {
    "classic": {"X": "X", "O": "O", "label": "Classic X/O", "price": 0},
    "emoji":   {"X": "❌", "O": "⭕", "label": "Emoji Pack", "price": 20},
    "sci":     {"X": "⚛️", "O": "🜂", "label": "Sci Pack", "price": 30},
    "fun":     {"X": "🐍", "O": "🦊", "label": "Fun Pack", "price": 40},
}

BACKGROUND_SETS = {
    "plain":  {"label": "Plain", "price": 0, "style": ""},
    "pastel": {"label": "Pastel", "price": 20, "style": "background-color:#f9f4ff;"},
    "dark":   {"label": "Dark", "price": 25, "style": "background-color:#111;color:#eee;"},
    "grid":   {"label": "Grid", "price": 30, "style": "background-image:linear-gradient(#ddd 1px, transparent 1px),linear-gradient(90deg,#ddd 1px,transparent 1px);background-size:20px 20px;"},
}

def symbol_display(s):
    pack = SYMBOL_SETS[st.session_state.symbol_skin]
    return pack[s] if s in pack else s

# ------------------------------
# UI helpers
# ------------------------------
def top_bar():
    cols = st.columns([0.5, 0.3, 0.2])
    with cols[0]:
        if st.session_state.username:
            st.markdown(f"**User:** {st.session_state.username}")
    with cols[1]:
        st.markdown(f"**Coins:** {st.session_state.coins}")
    with cols[2]:
        if st.button("Home"):
            st.session_state.page = "home"
            reset_board()

def reset_board():
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "X"
    st.session_state.game_over = False
    st.session_state.winner = None

def board_is_full():
    return all(cell != "" for row in st.session_state.board for cell in row)

def check_winner(symbol):
    b = st.session_state.board
    # Rows / cols
    for i in range(3):
        if b[i][0] == symbol and b[i][1] == symbol and b[i][2] == symbol:
            return True
        if b[0][i] == symbol and b[1][i] == symbol and b[2][i] == symbol:
            return True
    # Diagonals
    if b[0][0] == symbol and b[1][1] == symbol and b[2][2] == symbol:
        return True
    if b[0][2] == symbol and b[1][1] == symbol and b[2][0] == symbol:
        return True
    return False

def announce_result_and_route():
    # Route to result page with message and actions
    st.session_state.page = "result"

# ------------------------------
# Pages
# ------------------------------
def page_login():
    st.title("Welcome")
    st.write("Enter a username to start.")
    username = st.text_input("Username")
    if st.button("Continue"):
        if username.strip():
            st.session_state.username = username.strip()
            st.session_state.page = "home"
        else:
            st.warning("Please enter a valid username.")

def page_home():
    top_bar()
    st.title("Home")
    st.write("Select a mode:")
    cols = st.columns(3)
    with cols[0]:
        if st.button("Play vs Computer"):
            reset_board()
            st.session_state.mode = "cpu"
            st.session_state.page = "vs_cpu"
    with cols[1]:
        if st.button("Multiplayer (Local)"):
            reset_board()
            st.session_state.mode = "multi"
            st.session_state.page = "vs_multi"
    with cols[2]:
        if st.button("Shop"):
            st.session_state.page = "shop"

    st.divider()
    st.write("Tips:")
    st.write("- Win vs Computer to earn 10 coins.")
    st.write("- Use coins to buy symbol skins or background themes in the Shop.")

def render_board(on_click_cell):
    # Background style
    style = BACKGROUND_SETS[st.session_state.background_skin]["style"]
    if style:
        st.markdown(f"<div style='{style} padding:8px; border-radius:8px;'>", unsafe_allow_html=True)

    for i in range(3):
        row_cols = st.columns(3)
        for j in range(3):
            cell = st.session_state.board[i][j]
            label = symbol_display(cell) if cell else " "
            if row_cols[j].button(label, key=f"cell_{i}_{j}"):
                on_click_cell(i, j)

    if style:
        st.markdown("</div>", unsafe_allow_html=True)

def page_vs_cpu():
    top_bar()
    st.subheader("Tic-Tac-Toe vs Computer")
    st.write(f"Your symbol: {symbol_display('X')} | Computer: {symbol_display('O')}")

    def handle_click(i, j):
        if st.session_state.game_over:
            return
        if st.session_state.board[i][j] != "":
            return
        # Player move
        st.session_state.board[i][j] = "X"
        if check_winner("X"):
            st.session_state.game_over = True
            st.session_state.winner = "X"
            st.session_state.coins += 10
            announce_result_and_route()
            return
        if board_is_full():
            st.session_state.game_over = True
            st.session_state.winner = "Tie"
            announce_result_and_route()
            return
        # Computer move (random empty)
        empties = [(r,c) for r in range(3) for c in range(3) if st.session_state.board[r][c] == ""]
        if empties:
            r, c = random.choice(empties)
            st.session_state.board[r][c] = "O"
            if check_winner("O"):
                st.session_state.game_over = True
                st.session_state.winner = "O"
                announce_result_and_route()
                return
            if board_is_full():
                st.session_state.game_over = True
                st.session_state.winner = "Tie"
                announce_result_and_route()
                return

    render_board(handle_click)

    st.divider()
    cols = st.columns(2)
    with cols[0]:
        if st.button("Play Again"):
            reset_board()
            st.session_state.page = "vs_cpu"
    with cols[1]:
        if st.button("Home"):
            reset_board()
            st.session_state.page = "home"

def page_vs_multi():
    top_bar()
    st.subheader("Multiplayer (Local)")
    st.write("Alternate turns: X then O. No coins are awarded in multiplayer.")
    st.text_input("Player X name", value=st.session_state.p1_name, key="p1_name")
    st.text_input("Player O name", value=st.session_state.p2_name, key="p2_name")
    st.write(f"Turn: {st.session_state.p1_name if st.session_state.turn=='X' else st.session_state.p2_name} ({symbol_display(st.session_state.turn)})")

    def handle_click(i, j):
        if st.session_state.game_over:
            return
        if st.session_state.board[i][j] != "":
            return
        # Current player places symbol
        s = st.session_state.turn
        st.session_state.board[i][j] = s
        if check_winner(s):
            st.session_state.game_over = True
            st.session_state.winner = s
            announce_result_and_route()
            return
        if board_is_full():
            st.session_state.game_over = True
            st.session_state.winner = "Tie"
            announce_result_and_route()
            return
        # Switch turn
        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"

    render_board(handle_click)

    st.divider()
    cols = st.columns(2)
    with cols[0]:
        if st.button("Play Again"):
            reset_board()
            st.session_state.page = "vs_multi"
    with cols[1]:
        if st.button("Home"):
            reset_board()
            st.session_state.page = "home"

def page_result():
    top_bar()
    st.subheader("Match Result")
    if st.session_state.winner == "X":
        st.success(f"You won! +10 coins (Total: {st.session_state.coins})")
    elif st.session_state.winner == "O":
        if st.session_state.mode == "cpu":
            st.error("Computer wins!")
        else:
            who = st.session_state.p1_name if "X" == "O" else st.session_state.p2_name
            st.error("Player O wins!")
    else:
        st.info("It's a tie.")

    cols = st.columns(2)
    with cols[0]:
        if st.button("Play Again"):
            reset_board()
            # Return to mode page
            st.session_state.page = "vs_cpu" if st.session_state.mode == "cpu" else "vs_multi"
    with cols[1]:
        if st.button("Home"):
            reset_board()
            st.session_state.page = "home"

def page_shop():
    top_bar()
    st.subheader("Shop")
    st.write(f"Coins: {st.session_state.coins}")

    st.markdown("### Symbol Skins")
    for key, pack in SYMBOL_SETS.items():
        owned = key in st.session_state.owned_symbols
        cols = st.columns([0.5, 0.25, 0.25])
        with cols[0]:
            st.write(f"{pack['label']} — Price: {pack['price']} — Preview: {pack.get('X','X')} / {pack.get('O','O')}")
        with cols[1]:
            if owned:
                st.success("Owned")
            else:
                if st.button(f"Buy {pack['label']}", key=f"buy_sym_{key}"):
                    price = pack["price"]
                    if st.session_state.coins >= price:
                        st.session_state.coins -= price
                        st.session_state.owned_symbols.add(key)
                        st.success(f"Purchased {pack['label']}!")
                    else:
                        st.warning("Not enough coins.")
        with cols[2]:
            if owned:
                if st.button(f"Use {pack['label']}", key=f"use_sym_{key}"):
                    st.session_state.symbol_skin = key
                    st.info(f"Now using: {pack['label']}")

    st.markdown("### Background Themes")
    for key, theme in BACKGROUND_SETS.items():
        owned = key in st.session_state.owned_backgrounds
        cols = st.columns([0.5, 0.25, 0.25])
        with cols[0]:
            st.write(f"{theme['label']} — Price: {theme['price']}")
        with cols[1]:
            if owned:
                st.success("Owned")
            else:
                if st.button(f"Buy {theme['label']}", key=f"buy_bg_{key}"):
                    price = theme["price"]
                    if st.session_state.coins >= price:
                        st.session_state.coins -= price
                        st.session_state.owned_backgrounds.add(key)
                        st.success(f"Purchased {theme['label']}!")
                    else:
                        st.warning("Not enough coins.")
        with cols[2]:
            if owned:
                if st.button(f"Use {theme['label']}", key=f"use_bg_{key}"):
                    st.session_state.background_skin = key
                    st.info(f"Background set to: {theme['label']}")

    st.divider()
    if st.button("Back to Home"):
        st.session_state.page = "home"

# ------------------------------
# Router
# ------------------------------
def router():
    if st.session_state.page == "login":
        page_login()
    elif st.session_state.page == "home":
        page_home()
    elif st.session_state.page == "vs_cpu":
        page_vs_cpu()
    elif st.session_state.page == "vs_multi":
        page_vs_multi()
    elif st.session_state.page == "shop":
        page_shop()
    elif st.session_state.page == "result":
        page_result()
    else:
        st.session_state.page = "login"
        page_login()

router()
