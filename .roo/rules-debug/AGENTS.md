# Project Debug Rules (Non-Obvious Only)

- The DailyChallenge model has a unique constraint on ['challenge_type', 'date'] which causes IntegrityError when attempting to create duplicate challenges
- The update_daily_challenge_xp.py command has incorrect field references (start_date, end_date) that don't exist in the model
- Django timezone is set to Asia/Ho_Chi_Minh, so use timezone.now() for date/time operations
- Database is SQLite in development and PostgreSQL in production - environment variable DATABASE_URL determines which is used
- Static files are served differently in DEBUG vs production modes due to WhiteNoise configuration
- The NoCacheMiddleware prevents HTML caching in development mode
- Avatar uploads are handled through a specific upload_to path in the models
- Forum voting system uses multiple foreign key relationships that can cause complex query issues
- The unique_together constraint in SubjectPerformance model requires ('nguoi_dung', 'mon') combination to be unique