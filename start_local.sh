#!/bin/bash
# ============================================
# Script khởi động nhanh cho Linux/Mac
# ============================================

echo "========================================"
echo "  KHỞI ĐỘNG LOCAL DEVELOPMENT SERVER"
echo "========================================"
echo ""

# Kiểm tra file .env
if [ ! -f .env ]; then
    echo "[INFO] Tạo file .env từ .env.example..."
    cp .env.example .env
    echo "[OK] Đã tạo file .env"
    echo ""
fi

# Kiểm tra virtual environment
if [ ! -d venv ]; then
    echo "[INFO] Tạo virtual environment..."
    python3 -m venv venv
    echo "[OK] Đã tạo venv"
    echo ""
fi

# Kích hoạt virtual environment
echo "[INFO] Kích hoạt virtual environment..."
source venv/bin/activate

# Cài đặt dependencies
echo "[INFO] Cài đặt dependencies..."
pip install -r requirements.txt
echo ""

# Chạy migrations
echo "[INFO] Chạy database migrations..."
python manage.py makemigrations
python manage.py migrate
echo ""

# Tạo superuser nếu chưa có
echo "[INFO] Tạo superuser (nếu cần)..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>/dev/null || true
echo ""

# Collect static files
echo "[INFO] Thu thập static files..."
python manage.py collectstatic --noinput
echo ""

# Khởi động server
echo "========================================"
echo "  SERVER ĐANG CHẠY TẠI:"
echo "  http://localhost:8000"
echo "  http://127.0.0.1:8000"
echo "========================================"
echo ""
echo "Nhấn Ctrl+C để dừng server"
echo ""

python manage.py runserver
