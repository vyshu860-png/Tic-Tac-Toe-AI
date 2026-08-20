import streamlit as st
#Page configuration
st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="Game controller", layout="centered")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #120000, #450000);
}

.title {
    text-align: center;
    color: #ff2222;
    font-size: 45px;
    font-weight: bold;
    text-shadow: 0 0 15px red;
}

.score {
    background: #210000;
    border: 2px solid #ff2222;
    border-radius: 15px;
    padding: 12px;
    text-align: center;
    color: white;
}

.score b {
    color: #ff3333;
    font-size: 28px;
}

div.stButton > button {
    height: 100px;
    font-size: 42px;
    font-weight: bold;
    border-radius: 15px;
    background-color: #210000;
    color: white;
    border: 2px solid #ff3333;
}

div.stButton > button:hover {
    background-color: #600000;
    color: white;
    border: 2px solid white;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🎮 TIC-TAC-TOE AI</div>',
    unsafe_allow_html=True
)
st.title("Tic-Tac-Toe AI Game")
st.write("Welcome to the Tic-Tac-Toe AI game powered by minimax algorithm!.")
 #score variables        
if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0
#scoreboard
st.subheader("🏆 Scoreboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👤 You", st.session_state.player_score)

with col2:
    st.metric("🤖 AI", st.session_state.ai_score)

with col3:
    st.metric("🤝 Draws", st.session_state.draw_score) 
#Winning combinations

winning_combinations = [
    [0, 1, 2],  # Row 1
    [3, 4, 5],  # Row 2
    [6, 7, 8],  # Row 3
    [0, 3, 6],  # Column 1
    [1, 4, 7],  # Column 2
    [2, 5, 8],  # Column 3
    [0, 4, 8],  # Diagonal \
    [2, 4, 6]   # Diagonal /

]
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0
if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0

#check winner
def check_winner(board):
    for a,b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a]!= "":
            return board[a]
    if "" not in board:
        return "Tie"
    return None
#Minimax algorithm
def minimax(board, depth, is_maximizing):

    winner = check_winner(board)

    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "Tie":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score
    #Find best move for AI
def best_move(board):
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move
#Intialize game
if 'board' not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "message" not in st.session_state:
    st.session_state.message = "your turn! you are X"
    #reset game
def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.message = "your turn! you are X"
    
st.subheader("you: x | AI: o")
    #Display board
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        index = i * 3 + j
        display_value = st.session_state.board[index]
        if display_value == "x":
            display_value = "X"
        elif display_value == "o":
            display_value = "O"
        if cols[j].button(display_value or " ", key=index, use_container_width=True, disabled=st.session_state.game_over or st.session_state.board[index] != ""):
            if not st.session_state.game_over and st.        session_state.board[index] == "":
                st.session_state.board[index] = "X"
                

                winner = check_winner(st.session_state.board)

                if winner == "X":
                  st.session_state.player_score += 1
                  st.session_state.game_over = True
                  st.session_state.message = "🎉 You Win!"

                elif winner == "Tie":
                  st.session_state.draw_score += 1
                  st.session_state.game_over = True
                  st.session_state.message = "🤝 It's a Tie!"
                else:
                    ai_move = best_move(st.session_state.board)
                    if ai_move is not None:
                        st.session_state.board[ai_move] = "O"
                        winner = check_winner(st.session_state.board)

                        if winner == "O":
                          st.session_state.ai_score += 1
                          st.session_state.game_over = True
                          st.session_state.message = "🤖 AI Wins!"

                        elif winner == "Tie":
                           st.session_state.draw_score += 1
                           st.session_state.game_over = True
                           st.session_state.message = "🤝 It's a Tie!" 
                st.rerun()
st.markdown("---")
if st.button("Reset Game"):
    reset_game()
    st.rerun()

            