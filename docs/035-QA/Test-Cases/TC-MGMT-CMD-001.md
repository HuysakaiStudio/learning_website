---
id: TC-MGMT-CMD-001
type: test-case
status: draft
project: Django Learning Web App
owner: "@qa-team"
tags: [management-command, daily-challenges, update_daily_challenge_xp]
linked-to: [[DAILY_CHALLENGES_IMPLEMENTATION]]
created: 2026-04-11
updated: 2026-04-11
---

# Update Daily Challenge XP Management Command Test Case

## Overview
Test case to verify that the update_daily_challenge_xp management command works correctly without raising IntegrityError due to field mismatches.

## Pre-conditions
- Django application is running
- Database is accessible and migrated
- At least one user exists in the system
- Daily challenges exist for today's date

## Test Data
- Existing user account
- Daily challenges for today's date with various challenge types
- Mock data for user progress tracking

## Test Steps

### Step 1: Verify command runs without IntegrityError
1. Ensure daily challenges exist for today
2. Run the management command: `python manage.py update_daily_challenge_xp`
3. Verify command completes successfully
4. Check output for success message

### Step 2: Verify field mapping correctness
1. Check that command queries DailyChallenge using 'date' field (not 'start_date'/'end_date')
2. Verify UserChallengeProgress is accessed using correct field names ('current_value', 'completed_at', etc.)
3. Confirm challenge type matching works correctly ('exam', 'flashcard', 'streak', 'score', 'questions')

### Step 3: Verify user progress updates
1. Create test user with UserProfile
2. Create UserChallengeProgress records for today's challenges
3. Run command
4. Verify progress records are updated appropriately
5. Confirm XP is awarded correctly when challenges are completed

### Step 4: Test multiple users scenario
1. Create multiple test users
2. Run command
3. Verify all users' challenges are processed
4. Confirm no cross-user data contamination

## Expected Results
- Step 1: Command executes without IntegrityError or other exceptions
- Step 2: All field references match actual model definitions
- Step 3: User progress is updated correctly based on challenge completion
- Step 4: All users are processed independently

## Pass Criteria
- Management command executes successfully
- No database integrity errors occur
- User progress and XP are updated correctly
- All users processed without data contamination

## Fail Criteria
- IntegrityError during command execution
- FieldDoesNotExist or AttributeError exceptions
- Incorrect challenge completion detection
- Wrong XP calculation or assignment
- Cross-user data contamination

## Test Environment
- Local development environment
- SQLite database (as configured in settings)
- Django management command execution context