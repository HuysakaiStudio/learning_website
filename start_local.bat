@echo off
REM ============================================
REM Script khởi động nhanh cho Windows
REM ============================================

echo ========================================
echo   KHOI DONG LOCAL DEVELOPMENT SERVER
echo ========================================
echo.

REM Kiểm tra file .env
if not exist .env (
    echo [INFO] Tao file .env tu .env.example...
    copy .env.example .env
    echo [OK] Da tao file .env
    echo.
)

REM Kiểm tra virtual environment
if not exist venv (
    echo [INFO] Tao virtual environment...
    python -m venv venv
    echo [OK] Da tao venv
    echo.
)

REM Kích hoạt virtual environment
echo [INFO] Kich hoat virtual environment...
call venv\Scripts\activate.bat

REM Cài đặt dependencies
echo [INFO] Cai dat dependencies...
pip install -r requirements.txt
echo.

REM Chạy migrations
echo [INFO] Chay database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

REM Tạo superuser nếu chưa có
echo [INFO] Tao superuser (neu can)...
python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>nul
echo.

REM Collect static files
echo [INFO] Thu thap static files...
python manage.py collectstatic --noinput
echo.

REM Khởi động server
echo ========================================
echo   SERVER DANG CHAY TAI:
echo   http://localhost:8000
echo   http://127.0.0.1:8000
echo ========================================
echo.
echo Nhan Ctrl+C de dung server
echo.

python manage.py runserver
