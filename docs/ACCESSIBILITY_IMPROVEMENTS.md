# Accessibility Improvements Plan

## Overview
Fix accessibility issues to ensure the website is usable by everyone, including users with disabilities. Focus on WCAG 2.1 Level AA compliance.

## Issues to Fix

### 1. ARIA Labels
Add proper ARIA labels for interactive elements and screen readers.

### 2. Color Contrast
Ensure all text meets WCAG contrast ratios:
- Normal text: 4.5:1
- Large text (18pt+): 3:1

### 3. Keyboard Navigation
Ensure all interactive elements are keyboard accessible.

### 4. Focus Indicators
Add visible focus states for keyboard navigation.

### 5. Alt Text
Ensure all images have descriptive alt text.

## Implementation

### Base Template - Navigation
```html
<!-- templates/base.html -->

<!-- Add ARIA labels to navigation -->
<nav class="navbar navbar-expand-lg fixed-top shadow-sm bg-white" role="navigation" aria-label="Main navigation">
  <div class="container-fluid px-3">
    <a class="navbar-brand fw-bold text-primary" href="/" aria-label="Ôn Thi THPTQG - Trang chủ">
      <i class="bi bi-mortarboard-fill me-1" aria-hidden="true"></i>Ôn Thi THPTQG
    </a>

    <!-- Search form -->
    <form action="/search/" method="get" class="d-flex mx-3 flex-grow-1" style="max-width: 400px;" role="search">
      <label for="main-search" class="visually-hidden">Tìm kiếm</label>
      <input id="main-search" class="form-control" type="search" name="q" placeholder="Tìm kiếm..." aria-label="Tìm kiếm nội dung">
      <button type="submit" class="btn btn-primary ms-2" aria-label="Tìm kiếm">
        <i class="bi bi-search" aria-hidden="true"></i>
      </button>
    </form>

    <!-- User menu -->
    <div class="dropdown" aria-label="Menu người dùng">
      <button class="btn btn-link" id="userMenuButton" data-bs-toggle="dropdown" aria-expanded="false" aria-haspopup="true">
        <img src="..." alt="Avatar của {{ user.username }}" loading="lazy">
      </button>
      <ul class="dropdown-menu" aria-labelledby="userMenuButton">
        <!-- Menu items -->
      </ul>
    </div>
  </div>
</nav>
```

### Focus Indicators CSS
```css
/* static/css/accessibility.css */

/* Visible focus indicators */
*:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* Skip to main content link */
.skip-to-main {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--primary-500);
  color: white;
  padding: 8px 16px;
  text-decoration: none;
  z-index: 10000;
  border-radius: 0 0 4px 0;
}

.skip-to-main:focus {
  top: 0;
}

/* Visually hidden but accessible to screen readers */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Better focus for buttons */
button:focus,
a:focus,
input:focus,
select:focus,
textarea:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* Focus for cards */
.content-card:focus-within {
  box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.3);
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  * {
    border-color: currentColor !important;
  }
  
  button, a {
    text-decoration: underline;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Color Contrast Fixes
```css
/* Fix low contrast text */

/* Before: #999 on white (2.85:1) - FAIL */
/* After: #666 on white (5.74:1) - PASS */
.text-muted {
  color: #666 !important;
}

/* Before: Light blue on white - FAIL */
/* After: Darker blue - PASS */
.badge.bg-info {
  background-color: #0891b2 !important;
  color: white !important;
}

/* Ensure all badges have sufficient contrast */
.badge {
  font-weight: 600;
  padding: 6px 12px;
}

.badge.bg-light {
  background-color: #e5e7eb !important;
  color: #1f2937 !important;
}

/* Link contrast */
a {
  color: #1d4ed8; /* Darker blue for better contrast */
}

a:hover {
  color: #1e40af;
}

/* Button contrast */
.btn-outline-secondary {
  color: #374151;
  border-color: #6b7280;
}

.btn-outline-secondary:hover {
  background-color: #374151;
  border-color: #374151;
  color: white;
}
```

### Exam Page Accessibility
```html
<!-- templates/de_thi/lam_bai.html -->

<!-- Add ARIA labels to question palette -->
<div class="question-palette" role="navigation" aria-label="Danh sách câu hỏi">
  <div class="palette-header">
    <span class="palette-title" id="palette-title">Danh sách câu hỏi</span>
    <button class="palette-toggle" id="palette-toggle" aria-label="Thu gọn danh sách câu hỏi" aria-expanded="true">
      <i class="bi bi-chevron-right" aria-hidden="true"></i>
    </button>
  </div>

  <div class="palette-grid" id="palette-grid" role="list" aria-labelledby="palette-title">
    <!-- Question buttons with proper ARIA -->
  </div>
</div>

<!-- Question cards with proper structure -->
<div class="question-card" id="question-1" role="article" aria-labelledby="question-1-title">
  <h3 id="question-1-title" class="question-title">Câu 1</h3>
  <div class="question-content">
    <!-- Question text -->
  </div>
  
  <fieldset aria-labelledby="question-1-title">
    <legend class="visually-hidden">Chọn đáp án cho câu 1</legend>
    <div class="form-check">
      <input class="form-check-input" type="radio" name="cau_1" id="cau_1_a" value="A" aria-describedby="cau_1_a_label">
      <label class="form-check-label" for="cau_1_a" id="cau_1_a_label">
        A. Đáp án A
      </label>
    </div>
    <!-- More options -->
  </fieldset>
</div>

<!-- Timer with ARIA live region -->
<div class="timer" role="timer" aria-live="polite" aria-atomic="true">
  <span class="visually-hidden">Thời gian còn lại: </span>
  <span id="timer-display">45:00</span>
</div>

<!-- Submit button -->
<button type="button" onclick="nopBai()" class="btn btn-success" aria-label="Nộp bài thi">
  <i class="bi bi-check-circle" aria-hidden="true"></i> Nộp bài
</button>
```

### Form Accessibility
```html
<!-- Proper form labels and error messages -->
<div class="form-group">
  <label for="username" class="form-label">Tên đăng nhập <span class="text-danger" aria-label="bắt buộc">*</span></label>
  <input type="text" 
         id="username" 
         name="username" 
         class="form-control" 
         required 
         aria-required="true"
         aria-describedby="username-error username-help">
  <small id="username-help" class="form-text text-muted">Từ 3-20 ký tự</small>
  <div id="username-error" class="invalid-feedback" role="alert">
    Vui lòng nhập tên đăng nhập
  </div>
</div>
```

## Testing Checklist

### Automated Testing
- [ ] Run axe DevTools accessibility scan
- [ ] Run WAVE accessibility evaluation
- [ ] Run Lighthouse accessibility audit
- [ ] Check color contrast with WebAIM contrast checker

### Manual Testing
- [ ] Navigate entire site using only keyboard (Tab, Enter, Space, Arrow keys)
- [ ] Test with screen reader (NVDA on Windows, VoiceOver on Mac)
- [ ] Test with browser zoom at 200%
- [ ] Test in high contrast mode
- [ ] Test with reduced motion enabled

### Keyboard Navigation
- [ ] All interactive elements reachable via Tab
- [ ] Focus order is logical
- [ ] Focus indicators are visible
- [ ] Dropdowns work with arrow keys
- [ ] Modals can be closed with Escape
- [ ] Forms can be submitted with Enter

### Screen Reader
- [ ] All images have alt text
- [ ] All buttons have labels
- [ ] Form fields have labels
- [ ] Error messages are announced
- [ ] Page structure is logical (headings, landmarks)
- [ ] Dynamic content changes are announced

## Priority Fixes

### High Priority (Do Now)
1. Add ARIA labels to navigation
2. Fix color contrast issues
3. Add focus indicators
4. Add skip to main content link

### Medium Priority (This Week)
1. Add ARIA labels to all interactive elements
2. Improve form accessibility
3. Add keyboard shortcuts documentation
4. Test with screen readers

### Low Priority (Next Sprint)
1. Add ARIA live regions for dynamic content
2. Improve table accessibility
3. Add keyboard navigation hints
4. Create accessibility statement page

## Resources
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- axe DevTools: https://www.deque.com/axe/devtools/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
