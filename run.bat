@echo off
echo =========================================
echo    INICIANDO AMBIENTE STUDYFLOW
echo =========================================
echo.
echo [1] Iniciando Backend FastAPI na porta 8000...
start cmd /k "cd backend && call venv\Scripts\activate && uvicorn main:app --reload"
echo [2] Iniciando Frontend React (Vite) na porta 5173...
start cmd /k "cd frontend && npm run dev"
echo.
echo Os servidores foram abertos em novas janelas!
echo.
echo Para testar, abra no seu navegador:
echo Frontend (Telas): http://localhost:5173
echo Backend (Documentacao API): http://localhost:8000/docs
echo.
pause