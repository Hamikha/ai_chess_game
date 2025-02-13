import chess
import chess.svg
import streamlit as st
from autogen import ConversableAgent, register_function

# Initialize session state variables
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "made_move" not in st.session_state:
    st.session_state.made_move = False
if "board_svg" not in st.session_state:
    st.session_state.board_svg = None
if "move_history" not in st.session_state:
    st.session_state.move_history = []
if "game_active" not in st.session_state:
    st.session_state.game_active = False
if "human_color" not in st.session_state:
    st.session_state.human_color = "white"
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "game_status" not in st.session_state:
    st.session_state.game_status = ""

# Sidebar Configuration
st.sidebar.title("Chess Game Settings")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
if openai_api_key:
    st.session_state.openai_api_key = openai_api_key
    st.sidebar.success("API key saved!")

# Color selection
st.session_state.human_color = st.sidebar.radio(
    "Choose your color:",
    ("white", "black"),
    index=0 if st.session_state.human_color == "white" else 1
)

# Difficulty settings
difficulty = st.sidebar.select_slider(
    "AI Difficulty",
    options=["Beginner", "Intermediate", "Advanced"],
    value="Intermediate"
)

def check_made_move(msg):
    """Check if a move was made."""
    if st.session_state.made_move:
        st.session_state.made_move = False
        return True
    return False

def available_moves() -> str:
    """Get all legal moves in the current position."""
    moves = list(st.session_state.board.legal_moves)
    return "Available moves: " + ", ".join(move.uci() for move in moves)

def execute_move(move: str) -> str:
    """Execute a chess move."""
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move not in st.session_state.board.legal_moves:
            return f"Invalid move: {move}. Please check available moves."
        
        # Update board state
        st.session_state.board.push(chess_move)
        st.session_state.made_move = True

        # Generate board visualization with move highlighting
        board_svg = chess.svg.board(
            st.session_state.board,
            arrows=[(chess_move.from_square, chess_move.to_square)],
            fill={chess_move.from_square: "#aaa23b"},
            size=400
        )
        st.session_state.board_svg = board_svg
        
        # Get piece information
        piece_info = get_piece_info(chess_move)
        st.session_state.move_history.append({
            'board': board_svg,
            'move': move,
            'piece_moved': piece_info
        })

        # Check game status
        status = check_game_status()
        if status:
            st.session_state.game_over = True
            st.session_state.game_status = status
            return status

        return f"Move executed: {move} ({piece_info})"
    except ValueError as e:
        return f"Invalid move format: {move}. Use UCI format (e.g., 'e2e4'). Error: {str(e)}"
    except Exception as e:
        return f"Error executing move: {str(e)}"

def get_piece_info(move):
    """Get information about the moved piece."""
    piece = st.session_state.board.piece_at(move.from_square)
    if piece:
        piece_type = chess.piece_name(piece.piece_type).capitalize()
        color = "White" if piece.color else "Black"
        return f"{color} {piece_type}"
    return "Unknown piece"

def check_game_status():
    """Check the current game status."""
    if st.session_state.board.is_checkmate():
        winner = "White" if st.session_state.board.turn == chess.BLACK else "Black"
        return f"Checkmate! {winner} wins! 🏆"
    elif st.session_state.board.is_stalemate():
        return "Game ended in stalemate! 🤝"
    elif st.session_state.board.is_insufficient_material():
        return "Draw - insufficient material! 🤝"
    elif st.session_state.board.is_check():
        return "Check! ⚡"
    return None

def create_ai_agent(is_white):
    """Create an AI agent with appropriate configuration."""
    color = "white" if is_white else "black"
    personality = {
        "Beginner": "You are a novice chess player who sometimes makes mistakes. Analyze the position simply.",
        "Intermediate": "You are a skilled chess player who makes strategic moves. Analyze the position carefully.",
        "Advanced": "You are a chess grandmaster who plays aggressively and aims for victory. Analyze the position deeply."
    }
    
    return ConversableAgent(
        name=f"AI_{color.capitalize()}",
        system_message=f"{personality[difficulty]} You play as {color}. "
        "IMPORTANT: First call available_moves() to see valid moves, then call execute_move() with your chosen move in UCI format (e.g., 'e2e4').",
        llm_config={
            "config_list": [{
                "model": "gpt-4",
                "api_key": st.session_state.openai_api_key,
            }],
            "cache_seed": None
        },
    )

# Main game UI
st.title("♟️ Human vs AI Chess")

if st.session_state.openai_api_key:
    try:
        # Game controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start New Game"):
                st.session_state.board.reset()
                st.session_state.made_move = False
                st.session_state.move_history = []
                st.session_state.game_active = True
                st.session_state.game_over = False
                st.session_state.game_status = ""
                st.rerun()
        
        with col2:
            if st.button("Resign Game"):
                if st.session_state.game_active:
                    st.session_state.game_over = True
                    st.session_state.game_status = f"Game Over - {'Black' if st.session_state.human_color == 'white' else 'White'} wins by resignation!"
                    st.session_state.game_active = False

        # Display current game state
        if st.session_state.game_active and not st.session_state.game_over:
            st.subheader("Current Position")
            st.image(chess.svg.board(st.session_state.board, size=400))

            # Human move input
            if (st.session_state.board.turn == chess.WHITE and st.session_state.human_color == "white") or \
               (st.session_state.board.turn == chess.BLACK and st.session_state.human_color == "black"):
                
                st.write("Your turn! Make your move:")
                
                # Get and display legal moves
                legal_moves = [move.uci() for move in st.session_state.board.legal_moves]
                if not legal_moves:
                    st.error("No legal moves available!")
                else:
                    move = st.selectbox("Choose your move:", legal_moves)
                    if st.button("Make Move"):
                        result = execute_move(move)
                        st.write(result)
                        if not st.session_state.game_over:
                            st.rerun()
            
            # AI move
            else:
                st.write("AI is thinking... 🤔")
                ai_agent = create_ai_agent(st.session_state.board.turn == chess.WHITE)
                game_master = ConversableAgent(
                    name="Game_Master",
                    llm_config=False,
                    is_termination_msg=check_made_move,
                    human_input_mode="NEVER"
                )

                # Register functions for AI
                register_function(
                    execute_move,
                    caller=ai_agent,
                    executor=game_master,
                    description="Execute a chess move in UCI format (e.g., 'e2e4')"
                )
                register_function(
                    available_moves,
                    caller=ai_agent,
                    executor=game_master,
                    description="Get list of legal moves in current position"
                )

                # AI makes move
                chat_response = ai_agent.initiate_chat(
                    game_master,
                    message="Analyze the position and make your next move. Start by checking available moves.",
                    max_turns=3
                )
                
                if not st.session_state.made_move:
                    st.error("AI failed to make a move. Please try again.")
                else:
                    st.rerun()

        # Display game status
        if st.session_state.game_status:
            st.markdown(f"### {st.session_state.game_status}")

        # Move history
        if st.session_state.move_history:
            st.subheader("Move History")
            for i, move_data in enumerate(st.session_state.move_history):
                with st.expander(f"Move {i+1}: {move_data['piece_moved']} - {move_data['move']}"):
                    st.image(move_data['board'])

    except Exception as e:
        st.error(f"An error occurred: {str(e)}. Please check your API key and try again.")
else:
    st.warning("Please enter your OpenAI API key in the sidebar to start playing!")