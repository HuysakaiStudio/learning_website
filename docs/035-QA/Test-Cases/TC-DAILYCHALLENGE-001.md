---
id: TC-DAILYCHALLENGE-001
type: test-case
status: draft
project: Django Learning Web App
owner: "@qa-team"
tags: [daily-challenges, integrity-error, gamification]
linked-to: [[DAILY_CHALLENGES_IMPLEMENTATION]]
created: 2026-04-11
updated: 2026-04-11
---

# Daily Challenge Integrity Test Case

## Overview
Test case to verify that the DailyChallenge model properly handles the unique constraint on ['challenge_type', 'date'] to prevent IntegrityErrors.

## Pre-conditions
- Django application is running
- Database is accessible and migrated
- Test user account exists

## Test Data
- Challenge types: ['exam', 'flashcard', 'streak', 'score', 'questions']
- Test date: Today's date (will be generated during test execution)

## Test Steps

### Step 1: Verify unique constraint works correctly
1. Attempt to create a DailyChallenge with type 'exam' for today's date
2. Verify creation succeeds
3. Attempt to create another DailyChallenge with type 'exam' for today's date
4. Verify IntegrityError is raised

### Step 2: Verify different challenge types can coexist on same date
1. Create DailyChallenges for all 5 challenge types on the same date
2. Verify all creations succeed
3. Confirm 5 unique challenges exist for the date

### Step 3: Test update_daily_challenge_xp management command
1. Create test user with UserProfile
2. Generate daily challenges for today using generate_daily_challenges command
3. Run update_daily_challenge_xp command
4. Verify no IntegrityError occurs
5. Verify user challenge progress is updated correctly

### Step 4: Test concurrent challenge creation prevention
1. Simulate scenario where generate_daily_challenges might be run twice
2. Verify second run gracefully handles existing challenges
3. Confirm no duplicate challenges are created

## Expected Results
- Step 1: Second challenge of same type on same date should raise IntegrityError
- Step 2: All 5 different challenge types should be created successfully
- Step 3: Management command should execute without IntegrityError
- Step 4: Duplicate run should not create duplicates

## Pass Criteria
- Unique constraint properly enforced
- Management command executes without integrity errors
- No duplicate challenges created

## Fail Criteria
- IntegrityError when creating different challenge types on same date
- Successful creation of duplicate challenge types on same date
- IntegrityError during management command execution
- Duplicate challenges created by multiple command runs

## Test Environment
- Local development environment
- SQLite database (as configured in settings)