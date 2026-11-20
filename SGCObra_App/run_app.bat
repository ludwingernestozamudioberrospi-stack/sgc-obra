@echo off
title SGC Obra - Sistema de Control de Calidad
echo ========================================================
echo    INICIANDO SISTEMA DE GESTION DE PROTOCOLOS DE OBRA
echo    I.E. Jose Carlos Mariategui - Asistente de Obra
echo ========================================================
echo.
cd /d "%~dp0"
python -m uvicorn main:app --host 127.0.0.1 --port 8080 --reload
pause
