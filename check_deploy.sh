#!/bin/bash

# Script kiểm tra và chuẩn bị deploy
# Chạy: bash check_deploy.sh

echo "🔍 Kiểm tra chuẩn bị deploy..."
echo ""

# Màu sắc
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Kiểm tra file requirements.txt
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓${NC} requirements.txt tồn tại"
else
    echo -e "${RED}✗${NC} requirements.txt không tồn tại"
    echo "  Tạo file bằng: pip freeze > requirements.txt"
fi

# Kiểm tra file .env
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env tồn tại"
    
    # Kiểm tra SECRET_KEY
    if grep -q "SECRET_KEY=" .env; then
        echo -e "${GREEN}✓${NC} SECRET_KEY đã được set"
    else
        echo -e "${RED}✗${NC} SECRET_KEY chưa được set trong .env"
    fi
    
    # Kiểm tra DEBUG
    if grep -q "DEBUG=False" .env; then
        echo -e "${GREEN}✓${NC} DEBUG=False (production mode)"
    else
        echo -e "${YELLOW}⚠${NC} DEBUG không phải False (nên set False cho production)"
    fi
else
    echo -e "${RED}✗${NC} .env không tồn tại"
    echo "  Copy từ .env.example: cp .env.example .env"
fi

# Kiểm tra .gitignore
if [ -f ".gitignore" ]; then
    echo -e "${GREEN}✓${NC} .gitignore tồn tại"
    
    if grep -q ".env" .gitignore; then
        echo -e "${GREEN}✓${NC} .env đã được ignore"
    else
        echo -e "${RED}✗${NC} .env chưa được ignore"
    fi
    
    if grep -q "db.sqlite3" .gitignore; then
        echo -e "${GREEN}✓${NC} db.sqlite3 đã được ignore"
    else
        echo -e "${RED}✗${NC} db.sqlite3 chưa được ignore"
    fi
else
    echo -e "${RED}✗${NC} .gitignore không tồn tại"
fi

# Kiểm tra Procfile
if [ -f "Procfile" ]; then
    echo -e "${GREEN}✓${NC} Procfile tồn tại"
else
    echo -e "${YELLOW}⚠${NC} Procfile không tồn tại (cần cho Render/Railway)"
fi

# Kiểm tra runtime.txt
if [ -f "runtime.txt" ]; then
    echo -e "${GREEN}✓${NC} runtime.txt tồn tại"
else
    echo -e "${YELLOW}⚠${NC} runtime.txt không tồn tại (cần cho Render/Railway)"
fi

# Kiểm tra migrations
echo ""
echo "🔍 Kiểm tra migrations..."
if python manage.py showmigrations 2>/dev/null | grep -q "\[ \]"; then
    echo -e "${YELLOW}⚠${NC} Có migrations chưa chạy"
    echo "  Chạy: python manage.py migrate"
else
    echo -e "${GREEN}✓${NC} Tất cả migrations đã chạy"
fi

# Kiểm tra static files
echo ""
echo "🔍 Kiểm tra static files..."
if [ -d "staticfiles" ]; then
    echo -e "${GREEN}✓${NC} Folder staticfiles tồn tại"
else
    echo -e "${YELLOW}⚠${NC} Folder staticfiles chưa tồn tại"
    echo "  Chạy: python manage.py collectstatic"
fi

# Kiểm tra Git
echo ""
echo "🔍 Kiểm tra Git..."
if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository đã khởi tạo"
    
    # Kiểm tra remote
    if git remote -v | grep -q "origin"; then
        echo -e "${GREEN}✓${NC} Git remote đã được set"
        git remote -v
    else
        echo -e "${YELLOW}⚠${NC} Git remote chưa được set"
        echo "  Set remote: git remote add origin https://github.com/USERNAME/REPO.git"
    fi
else
    echo -e "${RED}✗${NC} Git chưa được khởi tạo"
    echo "  Khởi tạo: git init"
fi

# Tổng kết
echo ""
echo "================================"
echo "📋 CHECKLIST DEPLOY"
echo "================================"
echo ""
echo "Trước khi deploy, đảm bảo:"
echo "1. ✓ Đã test ứng dụng local"
echo "2. ✓ Đã set DEBUG=False trong .env"
echo "3. ✓ Đã tạo SECRET_KEY mới"
echo "4. ✓ Đã chạy migrations"
echo "5. ✓ Đã collectstatic"
echo "6. ✓ Đã push code lên GitHub"
echo ""
echo "Xem hướng dẫn chi tiết:"
echo "- QUICK_DEPLOY.md (Deploy nhanh PythonAnywhere)"
echo "- DEPLOYMENT_GUIDE.md (Hướng dẫn đầy đủ)"
echo ""
