# Project Documentation Rules (Non-Obvious Only)

- "apps/" directory contains all Django applications (kien_thuc, de_thi, nguoi_dung, etc.) rather than typical Django project structure
- "templates/" directory is in project root, not within individual apps, for centralized template management
- "static/" directory is in project root and serves all static files across the application
- Vietnamese language is primary (LANGUAGE_CODE = 'vi') with Asia/Ho_Chi_Minh timezone in settings
- "config/" directory contains Django settings rather than typical project root
- "avatars/" directory stores user avatars with specific upload handling
- "docs/" contains project documentation including ACCESSIBILITY_IMPROVEMENTS and DAILY_CHALLENGES_IMPLEMENTATION
- "plans/" contains redesign and improvement plans for the application
- "notifications/", "leaderboard/", "gamification/" are separate Django apps with specific functionality
- "studio/" app has its own configuration in apps.studio.apps.StudioConfig