# 🎓 Learning Web Platform

A comprehensive Django-based learning platform with flashcards, exams, leaderboards, and notifications.

---

## 🚀 Quick Start

```bash
# Activate virtual environment
venv\Scripts\activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit: http://localhost:8000

---

## ✨ Features

### 📚 Knowledge Management
- **Flashcards**: Spaced repetition learning system
- **Articles**: Educational content with moderation
- **Tags**: Organize content by topics

### 📝 Exam System
- **Multiple Question Types**: ABCD, True/False, Fill-in
- **Timed Exams**: Track completion time
- **Results Tracking**: Detailed performance analytics
- **Forum Discussion**: Discuss questions with peers
- **Anti-cheat**: Tab switching detection

### 🏆 Leaderboard System
- **Multiple Periods**: Daily, Weekly, Monthly, All-time
- **Categories**: Overall, Subject, Flashcard, Exam
- **Achievements**: Top 10, Top 100 badges
- **Auto-update**: Refreshes every hour

### 🔔 Notification System
- **8 Notification Types**: Achievement, Leaderboard, Exam, Forum, Flashcard, Study Reminder, Badge, System
- **Bell Widget**: Real-time unread count
- **Preferences**: Customize notification settings
- **API Endpoints**: For mobile/external integrations

### 👤 User Profiles
- **Badges**: Bronze, Silver, Gold achievements
- **Statistics**: Performance tracking
- **Avatar**: Profile customization

### 🎨 Studio
- **Content Creation**: Create flashcards and articles
- **Moderation**: Staff approval workflow
- **Analytics**: Track content performance

---

## 📊 Test Coverage

### Total: 29/29 tests PASSED ✅

- **Notifications**: 18 tests
- **Leaderboard**: 11 tests

Run tests:
```bash
python manage.py test
```

---

## 🗂️ Project Structure

```
learning-web/
├── apps/
│   ├── de_thi/          # Exam system
│   ├── kien_thuc/       # Knowledge & flashcards
│   ├── nguoi_dung/      # User profiles
│   ├── leaderboard/     # Rankings & achievements
│   ├── notifications/   # Notification system
│   └── studio/          # Content creation
├── config/              # Django settings
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── plans/               # Development roadmaps
│   ├── MASTER_PLAN.md
│   ├── one-night-development-plan.md
│   └── long-term-roadmap-3-6-months.md
├── IMPLEMENTATION_SUMMARY.md
├── TEST_RESULTS.md
└── manage.py
```

---

## 🔧 Technology Stack

### Backend
- **Django 5.2**: Web framework
- **SQLite**: Database (dev)
- **Python 3.10+**: Programming language

### Frontend
- **Bootstrap 5**: UI framework
- **Vanilla JavaScript**: Interactivity
- **MathJax**: Math rendering

### Features
- **Spaced Repetition**: Flashcard learning algorithm
- **Real-time Stats**: Session tracking
- **Responsive Design**: Mobile-friendly

---

## 📈 Performance

### Database Optimization
- ✅ 7 strategic indexes added
- ✅ Query optimization with select_related
- ✅ Bulk operations for efficiency

### Expected Performance
- Leaderboard queries: 50-70% faster
- User rank lookup: 60-80% faster
- Achievement queries: 40-60% faster

---

## 📚 Documentation

### For Users
- User guide (coming soon)
- FAQ (coming soon)

### For Developers
- [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md) - Recent changes
- [`TEST_RESULTS.md`](TEST_RESULTS.md) - Test coverage
- [`plans/MASTER_PLAN.md`](plans/MASTER_PLAN.md) - Development roadmap
- [`plans/README.md`](plans/README.md) - Plans navigation

---

## 🎯 Roadmap

### Completed ✅
- [x] Flashcard system with spaced repetition
- [x] Exam system with multiple question types
- [x] Leaderboard with rankings and achievements
- [x] Notification system (in-app)
- [x] User profiles and badges
- [x] Forum discussions
- [x] Content moderation
- [x] Comprehensive testing (29 tests)
- [x] Database optimization (7 indexes)

### Future Enhancements 🚀
See [`plans/long-term-roadmap-3-6-months.md`](plans/long-term-roadmap-3-6-months.md) for details:

**Month 1-2**:
- Email notifications with Celery
- Real-time updates with WebSockets
- Advanced analytics dashboard

**Month 3-4**:
- Mobile app (React Native)
- Push notifications
- Social features (follow, groups)

**Month 5-6**:
- AI-powered recommendations
- Gamification (XP, quests)
- Performance optimization

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python manage.py test`
5. Submit a pull request

---

## 📝 License

[Add your license here]

---

## 👥 Team

Developed with ❤️ by the Learning Web team

---

## 📞 Support

For issues and questions:
- Check documentation in [`plans/`](plans/)
- Review [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md)
- Run tests to verify setup

---

## 🎉 Status

**Current Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2026-04-08  
**Test Coverage**: 29/29 tests passing

---

**Happy Learning! 📚✨**
