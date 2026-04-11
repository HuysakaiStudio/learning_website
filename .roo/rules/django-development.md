---
trigger: glob
globs: "**/*.py"
description: Applied when editing Python/Django files to ensure proper Django conventions and best practices
---

# Django Development Standards

## 1. Executive Summary

All Django code must follow established Python and Django best practices, emphasizing maintainability, readability, and security.

## 2. Critical Constraints (The "Musts")

- 🔴 **NEVER** hardcode sensitive information in source code. Use environment variables or Django settings.
- 🔴 **NEVER** use raw SQL queries without proper validation. Always use Django ORM or parameterized queries.
- 🔴 **NEVER** import models directly from apps without proper referencing. Use `get_model()` when circular imports occur.

## 3. Code Patterns (The "How")

### Models

- Use `verbose_name` and `verbose_name_plural` in model Meta classes
- Always add `blank=True, null=True` for optional fields
- Use `choices` for field options instead of hardcoded values
- Implement `__str__` method for all models

### Views

- Use Class-Based Views (CBVs) when possible for better reusability
- Always validate forms and handle errors appropriately
- Use Django's permission decorators for access control
- Implement proper error handling and logging

### Forms

- Use Django forms for all user input validation
- Always override `clean_*` methods for custom validation
- Use form prefixes for multiple forms on the same page

### Templates

- Use template inheritance with base templates
- Apply proper escaping to prevent XSS attacks
- Use custom template tags for complex logic

### Example

✅ **Good**:

```python
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        
    def __str__(self):
        return self.title
```

❌ **Bad**:

```python
from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=10)  # No choices
    # Missing meta class and __str__ method