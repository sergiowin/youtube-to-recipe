@echo off
echo Starting Recipe Shorts App...

:: Start Backend Server
start cmd /k "cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python run.py"

:: Wait a moment for backend to initialize
timeout /t 5

:: Start Frontend Server
start cmd /k "cd frontend && npm install && npm run dev"

echo Application is starting up...
echo Backend will be available at http://127.0.0.1:5000
echo Frontend will be available at http://localhost:5173 