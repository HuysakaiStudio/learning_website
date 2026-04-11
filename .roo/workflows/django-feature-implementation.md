---
description: "Complete end-to-end implementation of a new Django feature from specification to testing"
---

# Django Feature Implementation Workflow

## 1. Initialization

1. Load Global Rules: `documents.md`, `django-development.md`.
2. Analyze Context: Identify affected Django apps and components.

## 2. Phase I: Specification (The "PM" Phase)

> 💡 **Tip**: Clarify requirements before coding.

1. Invoke **[product-manager]** to refine feature requirements.
   // turbo
2. Create `docs/020-Requirements/Feature-{FeatureName}.md`.
3. **WAIT** for user approval of requirements.

## 3. Phase II: Architecture (The "Architect" Phase)

1. Read `docs/020-Requirements/Feature-{FeatureName}.md`.
2. Invoke **[lead-architect]** to create `docs/030-Specs/Architecture/{FeatureName}-Architecture.md`.
3. Define data models, API endpoints, and UI components needed.
4. **WAIT** for user approval of architecture.

## 4. Phase III: Implementation (The "Dev" Phase)

1. Read `docs/030-Specs/Architecture/{FeatureName}-Architecture.md`.
2. Invoke **[backend-developer]** to implement models and views.
3. Create/modify Django models in appropriate apps.
4. Create/modify Django views and URL patterns.
5. Invoke **[frontend-developer]** to implement UI components.
6. Create/update HTML templates and CSS files.
7. Create/modify forms as needed.

## 5. Phase IV: Testing (The "QA" Phase)

1. Invoke **[qa-tester]** to create test cases.
2. Write unit tests for models and views.
3. Write integration tests for feature functionality.
4. Run complete test suite using `python manage.py test`.
5. **WAIT** for test results verification.

## 6. Phase V: Documentation & Review

1. Update documentation in `docs/060-Manuals/User-Guide/` if needed.
2. Create/update API documentation if applicable.
3. Perform code review and address feedback.
4. Merge changes to main branch.