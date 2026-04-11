# Project Architecture Rules (Non-Obvious Only)

- Multi-app Django structure with apps in "apps/" directory (kien_thuc, de_thi, nguoi_dung, leaderboard, notifications, gamification)
- Centralized templates in project root "templates/" directory rather than distributed per app
- User authentication and profiles managed through nguoi_dung app with custom UserProfile model
- Gamification system implemented through separate app with DailyChallenge and UserChallengeProgress models
- Leaderboard functionality separated into its own app with Achievement and LeaderboardEntry models
- Forum system embedded within de_thi app for question discussions
- Flashcard system in kien_thuc app with spaced repetition algorithm implementation
- Practice session tracking system for waypoint-style learning progression
- Notification system as standalone app with preferences and real-time updates
- Database constraints include unique_together on DailyChallenge preventing duplicate challenge types per date
- Custom middleware (NoCacheMiddleware) prevents HTML caching in development
- Static file serving configured with WhiteNoise for both development and production
- Environment-based configuration switches between SQLite (dev) and PostgreSQL (prod)
- Custom context processor (cache_buster) for cache invalidation strategies