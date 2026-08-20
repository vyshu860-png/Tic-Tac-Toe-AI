import streamlit as st
#Page configuration
st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="Game controller", layout="centered")
st.title ("Tic-Tac-Toe AI")
st.write("Welcome to the Tic-Tac-Toe AI game powered by minimax algorithm!. Choose your symbol and make your move. The AI will respond with its move. Try to win the game!")

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
#check winner
def check_winner(board):
    for a,b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a]!= "":
            return board[a]
    if "" not in board:
        return "draw"
    return None
#Minimax algorithm
def minimax(board, depth, is_maximizing):

    winner = check_winner(board)

    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "draw":
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
            if not st.session_state.game_over and st.session_state.board[index] == "":
                st.session_state.board[index] = "X"
                winner = check_winner(st.session_state.board)
                if winner:
                    st.session_state.game_over = True
                    if winner == "draw":
                        st.session_state.message = "It's a draw!"
                    else:
                        st.session_state.message = f"{winner} wins!"
                else:
                    ai_move = best_move(st.session_state.board)
                    if ai_move is not None:
                        st.session_state.board[ai_move] = "O"
                        winner = check_winner(st.session_state.board)
                        if winner:
                            st.session_state.game_over = True
                            if winner == "O":
                                st.session_state.message = "AI wins!"
                            elif winner == "draw":
                                st.session_state.message = "It's a draw!"
                            else:
                                st.session_state.message = f"{winner} wins!"
                st.rerun()
st.markdown("---")
if st.button("Reset Game"):
    reset_game()
    st.rerun()

            