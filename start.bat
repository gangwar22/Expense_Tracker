@echo off
title Expense Tracker Launcher
echo ===================================================
echo   Starting Expense Tracker (FastAPI + React)
echo ===================================================

echo [1/2] Starting Backend API (FastAPI)...
start "Backend - FastAPI" cmd /k "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting Frontend UI (React + Vite)...
cd frontend
start "Frontend - React" cmd /k "npm run dev"

echo.
echo ===================================================
echo  Both servers have been launched!
echo  Backend Docs: http://127.0.0.1:8000/docs
echo  Frontend UI:   http://localhost:5173
echo ===================================================
