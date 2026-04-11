---
id: TC-OFFLINE-ISSUE-001
type: test-case
status: draft
project: Django Learning Web App
owner: "@qa-team"
tags: [offline, connectivity, leaderboard, admin]
linked-to: []
created: 2026-04-11
updated: 2026-04-11
---

# Offline Issue Test Case - Leaderboard and Admin Pages

## Overview
Test case to verify why leaderboard and admin pages are showing as offline when they should be accessible.

## Pre-conditions
- Django development server is running
- Application is accessible locally
- Internet connection is available for local development

## Test Data
- Local server URL: http://localhost:8000 or as configured
- Admin URL: /admin/
- Leaderboard URL: /leaderboard/ (or equivalent)

## Test Steps

### Step 1: Verify server is running
1. Check if Django development server is running
2. Verify the server is listening on the correct port
3. Confirm the server process is active

### Step 2: Test basic page accessibility
1. Navigate to homepage
2. Verify basic pages load correctly
3. Check if static files are loading

### Step 3: Test leaderboard page specifically
1. Navigate to leaderboard URL
2. Check browser console for errors
3. Inspect network tab for failed requests
4. Verify if it's a client-side offline detection or actual server issue

### Step 4: Test admin page specifically
1. Navigate to admin URL
2. Check browser console for errors
3. Inspect network tab for failed requests
4. Verify if authentication is required

### Step 5: Check PWA/offline functionality
1. Check if service worker is registered
2. Verify if PWA offline detection is interfering
3. Look for sw.js (service worker) file

### Step 6: Check for network connectivity detection
1. Look for JavaScript code that detects online/offline status
2. Check if there's a connectivity check that's incorrectly reporting offline status

## Expected Results
- Server should be running and accessible
- All pages including leaderboard and admin should be accessible
- No false offline detection should occur

## Pass Criteria
- All pages load without "offline" messages
- Network requests complete successfully
- Service worker doesn't interfere with page loading

## Fail Criteria
- Pages show "offline" messages when online
- Network requests fail
- Service worker incorrectly reports offline status

## Test Environment
- Local development environment
- Chrome/Firefox browser for inspection