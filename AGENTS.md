# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Django Learning Web Application

This is a Vietnamese educational platform for exam preparation with features for flashcards, exams, leaderboards, and gamification.

## Build/Lint/Test Commands

- Run development server: `python manage.py runserver`
- Run tests: `python manage.py test` (all tests) or `python manage.py test apps.{app_name}` for specific app
- Run specific test: `python manage.py test apps.de_thi.tests` (replace with specific test module)
- Create migration: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Collect static files: `python manage.py collectstatic --noinput`
- Check for issues: `python manage.py check`

## Code Style Guidelines

- Use Vietnamese for model field names and English for code/logic
- Models use `verbose_name` and `verbose_name_plural` in Vietnamese
- Follow Django naming conventions: snake_case for fields/methods
- Use `related_name` in ForeignKey relationships
- Always specify `on_delete` for ForeignKey fields
- Use `null=True, blank=True` for optional fields
- Use `BigAutoField` as default primary key
- Use `unique_together` constraints as needed (like in DailyChallenge model)
- Date/time fields use Asia/Ho_Chi_Minh timezone

## Project-Specific Patterns

- Apps are organized in the `apps/` directory with names like `kien_thuc`, `de_thi`, `nguoi_dung`
- Templates are in the root `templates/` directory
- Static files are in the root `static/` directory
- The `unique_together` constraint in `DailyChallenge` model prevents duplicate challenge types on the same date
- Custom management commands are in `apps/{app}/management/commands/`
- The project uses a custom context processor in `config.context_processors.cache_buster`
- Middleware includes `NoCacheMiddleware` to prevent HTML caching in development
- Internationalization uses Vietnamese (vi) as the primary language

## Critical Gotchas

- The DailyChallenge model has a unique constraint on `['challenge_type', 'date']` which prevents duplicate challenges of the same type on the same date
- When creating daily challenges, check if challenges already exist for the date to avoid IntegrityError
- The `update_daily_challenge_xp.py` command has incorrect field references (`start_date`, `end_date`) that don't exist in the model
- Use `timezone.now().date()` for date comparisons in the DailyChallenge model
- Avatar images are stored in the `avatars/` directory