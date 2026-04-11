---
description: "Standard process for creating new Django models with proper validation, testing, and documentation"
---

# Django Model Creation Workflow

## 1. Initialization

1. Load Global Rules: `documents.md`, `django-development.md`, `clean-code.md`.
2. Identify the app where the model will be created: `apps/{app_name}/models.py`.

## 2. Phase I: Requirements Analysis

1. Define the purpose of the new model and its relationships.
2. Identify required fields and their types.
3. Determine any constraints, indexes, or validation rules needed.
4. **WAIT** for requirements confirmation.

## 3. Phase II: Model Design

1. Invoke **[lead-architect]** to review model design.
2. Define model fields with appropriate types and constraints.
3. Add proper `verbose_name` and `verbose_name_plural` in Meta class.
4. Implement `__str__` method for human-readable representation.
5. Define model relationships (ForeignKey, ManyToMany, etc.) correctly.
6. Add any custom model methods as needed.
7. **WAIT** for design approval.

## 4. Phase III: Implementation

1. Create the model in the appropriate app's `models.py` file.
2. Follow Django naming conventions and best practices.
3. Add proper docstrings for the model and complex fields.
4. Include any custom managers if needed.
5. Ensure proper imports at the top of the file.

## 5. Phase IV: Migration & Testing

1. Create Django migration using `python manage.py makemigrations`.
2. Review migration file for correctness.
3. Apply migration using `python manage.py migrate`.
4. Create comprehensive tests for the model in `tests.py`:
   - Test model creation and basic properties
   - Test custom methods
   - Test validation constraints
   - Test relationships with other models
5. Run the tests using `python manage.py test`.

## 6. Phase V: Integration & Documentation

1. Update admin interface if the model should be admin-editable.
2. Create/update forms if users will interact with the model.
3. Add documentation for the new model in relevant docs.
4. Update any related views or templates that use the model.
5. Verify that the model integrates properly with the rest of the system.