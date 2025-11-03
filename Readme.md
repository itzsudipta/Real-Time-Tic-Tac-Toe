# Real-Time Tic Tac Toe - Python Backend

A robust backend system for a real-time Tic Tac Toe game that provides intelligent move suggestions using the Minimax algorithm. This API helps users make optimal moves by analyzing the game board and computing the best possible strategy.

# Collaboration

This repository is part of a collaborative group project and is currently under development. Contributions and integration with the frontend are ongoing.

## 🎯 Overview

This backend service implements game theory principles through the **Minimax Algorithm** to deliver unbeatable AI move suggestions. The algorithm recursively evaluates all possible game states to determine the optimal next move for the player.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI server)
- **Validation**: Pydantic
- **Deployment**: Render

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Real Time TicTac"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

## 🔌 API Usage

### Endpoint: `/get_best_move`

**Method**: `POST`

**Request Body**:
```json
{
  "board": ["X", "O", " ", "X", " ", "O", " ", " ", " "]
}
```

**Response** (Success):
```json
{
  "success": true,
  "best_move": 4
}
```
**Response** (Error):
```json
{
  "success": false,
  "message": "No valid moves found or error occurred."
}
```
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Development Status

🚧 **Under Development** - This project is actively being developed. Features and API may change.

---

**Note**: The AI is designed to play optimally. When playing as 'X', it will never lose if it plays first.