# Human vs AI Chess Game
A Streamlit-based interactive chess game where humans can play against an AI opponent powered by GPT-4. The game features adjustable difficulty levels, move visualization, and detailed game history.

## Features
- 🎮 Interactive chess board with move highlighting
- 🤖 AI opponent with adjustable difficulty levels (Beginner, Intermediate, Advanced)
- 🎨 Choice of playing as White or Black
- 📝 Detailed move history with board positions
- ⚡ Real-time game status updates
- 🎯 Legal move validation and suggestions
- 🏆 Game outcome detection (checkmate, stalemate, insufficient material)

## Prerequisites
- Python 3.7+
- OpenAI API key
- Required Python packages:
  ```
  streamlit
  chess
  autogen
  ```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chess-game
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a requirements.txt file with the following contents:
```
streamlit
chess
autogen
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run chess_game.py
```

2. In your web browser:
   - Enter your OpenAI API key in the sidebar
   - Choose your preferred color (White/Black)
   - Select AI difficulty level
   - Click "Start New Game" to begin playing

## Game Controls

- **Start New Game**: Resets the board and starts a fresh game
- **Resign Game**: Forfeit the current game
- **Move Selection**: Choose from available legal moves in UCI format (e.g., 'e2e4')
- **Move History**: Expand move entries to see board positions

## AI Difficulty Levels

- **Beginner**: Makes occasional mistakes, plays more straightforward moves
- **Intermediate**: Plays strategically, considers positional advantages
- **Advanced**: Plays aggressively, aims for tactical complications

## Technical Details

The game uses several key components:
- **Streamlit**: For the web interface and state management
- **python-chess**: For chess rules and board representation
- **AutoGen**: For AI agent behavior and decision making
- **OpenAI GPT-4**: For move analysis and generation

## Game Features

### Move Validation
- All moves are validated against chess rules
- Only legal moves are presented as options
- Invalid moves are caught and reported with clear error messages

### Board Visualization
- Current position display
- Move highlighting with arrows
- Color-coded previous move squares

### Game State Tracking
- Checkmate detection
- Stalemate detection
- Insufficient material detection
- Check indication

### Move History
- Complete game record
- Board position for each move
- Piece movement details
- Expandable move list with visualizations

## Error Handling

The game includes comprehensive error handling for:
- Invalid moves
- API connection issues
- Game state inconsistencies
- Move execution failures

## Limitations

- Requires an active internet connection
- OpenAI API key needed
- API costs associated with GPT-4 usage
- Move analysis time varies based on position complexity

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Future Improvements

Planned features:
- PGN export/import
- Opening book integration
- Time controls
- Position analysis
- Move suggestions for learning
- Multiplayer support


## Acknowledgments

- Thanks to the python-chess library developers
- Thanks to the Streamlit team
- Thanks to Anthropic for GPT-4 integration
- Thanks to the AutoGen team for the agent framework
- Thanks to https://github.com/Shubhamsaboo

## Support

For support, please:
1. Check existing issues on the repository
2. Create a new issue with detailed problem description
3. Include error messages and steps to reproduce any bugs

## Author

Hammad Ahmad

---
Last Updated: February 2025