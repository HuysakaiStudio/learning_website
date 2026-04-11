# CSS Refactoring Plan for Flashcard and Practice Modes

## Overview
This document outlines the refactoring of CSS classes to prevent conflicts between flashcard and practice modes in the learning web application. The main objective is to implement namespaced CSS classes that avoid style collisions.

## Problem Statement
The application had CSS conflicts between flashcard and practice modes due to generic class names that affected both components simultaneously. This caused unexpected styling issues and made maintenance difficult.

## Solution Approach
Implemented namespaced CSS classes with the `kt-` prefix (for "knowledge training") to ensure all flashcard and practice mode components have unique, non-conflicting styles.

## Changes Made

### 1. New CSS File Created
- **File**: `static/css/flashcard-styles.css`
- **Purpose**: Contains all refactored styles for flashcard and practice modes with namespaced classes
- **Features**:
  - Scoped CSS classes prefixed with `kt-`
  - Complete styling for flashcard components
  - Complete styling for practice mode components
  - Dark mode support for all new components
  - Responsive adaptations

### 2. Template Updates

#### Flashcard Template (`templates/kien_thuc/hoc_flashcard.html`)
Updated class names to use the new namespaced classes:

| Old Class | New Class |
|-----------|-----------|
| `.study-container` | `.kt-flashcard-container` |
| `.study-header` | `.kt-study-header` |
| `.progress-container` | `.kt-progress-container` |
| `.progress-info` | `.kt-progress-info` |
| `.progress-bar` | `.kt-progress-bar` |
| `.progress-fill` | `.kt-progress-fill` |
| `.session-stats` | `.kt-stats-container` |
| `.session-stats-grid` | `.kt-session-stats-grid` |
| `.session-stat` | `.kt-session-stat` |
| `.session-stat-value` | `.kt-session-stat-value` |
| `.session-stat-label` | `.kt-session-stat-label` |
| `.card-container` | `.kt-card-container` |
| `.flashcard-card` | `.kt-flashcard-card` |
| `.bookmark-btn` | `.kt-bookmark-btn` |
| `.card-face` | `.kt-card-face` |
| `.card-front` | `.kt-card-front` |
| `.card-back` | `.kt-card-back` |
| `.hint-text` | `.kt-hint-text` |
| `.flashcard-controls` | `.kt-flashcard-controls` |
| `.mode-switch` | `.kt-mode-switch` |
| `.flashcard-btn` | `.kt-flashcard-btn` |
| `.btn-flip` | `.kt-btn-flip` |
| `.btn-again` | `.kt-btn-again` |
| `.btn-hard` | `.kt-btn-hard` |
| `.btn-good` | `.kt-btn-good` |
| `.btn-easy` | `.kt-btn-easy` |
| `.mode-toggle` | `.kt-mode-toggle` |
| `.mode-btn` | `.kt-mode-btn` |
| `.completion-message` | `.kt-completion-message` |

#### Practice Mode Template (`templates/de_thi/luyen_tung_cau.html`)
Updated class names to use the new namespaced classes:

| Old Class | New Class |
|-----------|-----------|
| `.practice-header` | `.kt-practice-header` |
| `.progress-bar-container` | `.kt-progress-bar-container` |
| `.progress-bar-fill` | `.kt-progress-bar-fill` |
| `.choice-option` | `.kt-choice-option` |
| `.choice-letter` | `.kt-choice-letter` |
| `.ds-option` | `.kt-ds-option` |
| `.feedback-overlay` | `.kt-feedback-overlay` |
| `.feedback-card` | `.kt-feedback-card` |
| `.result-text` | `.kt-result-text` |
| `.answer-section` | `.kt-answer-section` |
| `.explanation-section` | `.kt-explanation-section` |

### 3. JavaScript Updates
Updated JavaScript code to reference the new class names for event listeners and DOM manipulation.

## Benefits of Refactoring

### 1. Eliminated CSS Conflicts
- Namespaced classes prevent style bleeding between components
- Each component now has its own isolated styling scope
- No more unintended style inheritance between flashcards and practice modes

### 2. Improved Maintainability
- Clear class naming convention makes code more readable
- Easier to locate and modify specific component styles
- Reduced risk of introducing bugs when updating styles

### 3. Enhanced Scalability
- New components can be added without worrying about style conflicts
- Consistent naming pattern makes it easy to extend functionality
- Modular approach allows for component reuse

### 4. Better Performance
- More specific selectors improve rendering efficiency
- Reduced CSS cascade complexity
- Optimized for modern browsers

## Dark Mode Support
All new CSS classes include proper dark mode support with appropriate variable mappings and fallbacks. The dark mode styles follow the same namespaced approach to maintain consistency.

## Responsive Design
The new CSS includes responsive adaptations for different screen sizes while maintaining the namespaced class structure.

## Testing Recommendations
After implementing these changes, it's recommended to test:

1. Flashcard functionality on different devices and screen sizes
2. Practice mode functionality across various scenarios
3. Dark mode compatibility for both components
4. Cross-browser compatibility
5. Performance impact of the new CSS structure

## Rollback Plan
If issues arise, the rollback plan involves:
1. Removing the new CSS file (`static/css/flashcard-styles.css`)
2. Reverting template class names to their original values
3. Updating the base template to remove the CSS reference

## Conclusion
This refactoring successfully addresses CSS conflicts between flashcard and practice modes while establishing a scalable foundation for future development. The namespaced approach ensures clean separation of concerns and improves overall code quality.