# Project Coding Rules (Non-Obvious Only)

- Always use Vietnamese for model field names and database-related content, but use English for code logic
- Models must use `verbose_name` and `verbose_name_plural` in Vietnamese following Django conventions
- Use `related_name` in all ForeignKey relationships to enable reverse lookups
- Always specify `on_delete` parameter for ForeignKey fields (commonly `models.CASCADE`, `models.SET_NULL`, or `models.PROTECT`)
- Use `null=True, blank=True` for optional fields to allow empty values in both database and forms
- The DailyChallenge model has a unique constraint on `['challenge_type', 'date']` that prevents duplicate challenges of the same type on the same date
- Date/time fields use Asia/Ho_Chi_Minh timezone (`TIME_ZONE = 'Asia/Ho_Chi_Minh'`) so use `timezone.now()` for datetime operations
- Avatar images are stored in the `avatars/` directory with specific upload handling
- The `update_daily_challenge_xp.py` command has incorrect field references that need to be fixed (missing `start_date`, `end_date` fields in the model)
- Custom management commands are located in `apps/{app}/management/commands/` following Django convention
- Use `BigAutoField` as default primary key as configured in settings