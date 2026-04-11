---
description: "Test-Driven Development cycle for Django development: write tests first, then implement, then verify"
---

# Django Test-Driven Development Cycle

## 1. Initialization

1. Load Global Rules: `tests.md`, `django-development.md`.
2. Identify the component that needs development/testing.

## 2. Phase I: Test Definition (The "QA" Phase)

> 💡 **Tip**: Define expected behavior before implementation.

1. Invoke **[qa-tester]** to analyze the feature/bug requirements.
2. Write a failing test case that reproduces the bug or defines the expected behavior.
3. Ensure test covers edge cases and error conditions.
4. Run the test to confirm it fails as expected.
   ```bash
   python manage.py test {app_name}.{test_module}.{TestClass}.{test_method}
   ```
5. **WAIT** for test creation confirmation.

## 3. Phase II: Implementation (The "Developer" Phase)

1. Read the failing test to understand requirements.
2. Invoke **[backend-developer]** to implement minimal code to pass the test.
3. Focus only on making the specific test pass.
4. Refrain from adding extra functionality during this phase.
5. Follow Django best practices and coding standards.

## 4. Phase III: Verification & Refinement

1. Run the test again to verify it passes.
2. Run the full test suite to ensure no regressions.
3. If test passes, refactor code for clarity and efficiency.
4. If test fails, return to implementation phase.
5. Add additional test cases for edge cases discovered during implementation.

## 5. Phase IV: Integration Testing

1. Write integration tests to verify the new functionality works with other components.
2. Test the feature end-to-end if applicable.
3. Run complete test suite one final time.
4. **WAIT** for all tests to pass before marking the task complete.