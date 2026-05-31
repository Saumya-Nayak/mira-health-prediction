# MIRA - Medical Intelligence Robotic Automation

A health prediction web application built with Python and Flask.

## Tech Stack

- Backend: Python, Flask, Flask-SQLAlchemy
- Database: SQLite
- AI Integration: OpenRouter API
- Frontend: HTML5, CSS3

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add: `OPENROUTER_API_KEY=your_key_here`
4. Run: `python app.py`
5. Open: `http://127.0.0.1:5000`

## Features

- Add, view, edit and delete patient records
- Input validation for all fields
- AI-generated health risk assessment via OpenRouter API
- Persistent SQLite storage
