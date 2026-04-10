# Learning Website - Django Project

## Project Overview
Ứng dụng web học tập THPT Quốc Gia với các tính năng:
- Đề thi trắc nghiệm
- Flashcard học tập
- Bài viết kiến thức
- Hệ thống gamification (XP, Level, Streak)
- Leaderboard và thành tích
- Dark mode
- PWA support

## Tech Stack
- Django 5.2.12
- Python 3.12
- SQLite (development) / PostgreSQL (production)
- Bootstrap 5.3.3
- MathJax 3 (render công thức toán)

## Development Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Run Server
```bash
python manage.py runserver
```

### Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py them_mon_mac_dinh  # Thêm môn học mặc định
```

### Static Files
```bash
python manage.py collectstatic --noinput
```

## Project Structure
```
learning_website/
├── apps/
│   ├── de_thi/          # Đề thi và bài thi
│   ├── kien_thuc/       # Bài viết, flashcard
│   ├── nguoi_dung/      # User profiles
│   ├── leaderboard/     # XP, achievements
│   ├── notifications/   # Thông báo
│   └── studio/          # Video content
├── config/              # Django settings
├── templates/           # HTML templates
├── static/              # CSS, JS, images
└── media/               # User uploads
```

## Gstack Integration
Gstack đã được cài đặt tại `skills/gstack/`. Sử dụng các skills:
- `/office-hours` - Brainstorm ideas
- `/investigate` - Debug bugs
- `/ship` - Create PR
- `/qa` - Test website
- `/review` - Code review

## Deployment
- PythonAnywhere: WSGI configuration
- Render/Railway: Dockerfile ready
- Vercel: Static files only

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
