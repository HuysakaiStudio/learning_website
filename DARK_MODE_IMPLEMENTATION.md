# Dark Mode Implementation

## Tổng Quan

Đã triển khai hệ thống Dark Mode hoàn chỉnh cho toàn bộ website với các tính năng:

- ✅ Chuyển đổi mượt mà giữa chế độ sáng và tối
- ✅ Lưu trữ preference trong localStorage
- ✅ Tự động phát hiện system preference
- ✅ Nút toggle đẹp mắt trên navbar
- ✅ Tương thích với tất cả components hiện có

## Files Đã Tạo

### 1. [`static/css/dark-mode.css`](static/css/dark-mode.css)
File CSS chứa tất cả styles cho dark mode:
- Color variables cho dark theme
- Styles cho navbar, cards, forms, tables
- Styles cho buttons, alerts, badges
- Scrollbar styling
- Toggle button animation

### 2. [`static/js/dark-mode.js`](static/js/dark-mode.js)
JavaScript xử lý logic dark mode:
- Khởi tạo từ localStorage
- Toggle function
- Lắng nghe system preference changes
- Export API để sử dụng từ code khác

### 3. [`templates/base.html`](templates/base.html:13)
Đã cập nhật:
- Thêm link đến dark-mode.css
- Thêm script dark-mode.js
- Thêm nút toggle trên navbar

## Cách Sử Dụng

### Cho Người Dùng

1. Nhấn vào nút toggle (☀️/🌙) trên navbar
2. Preference được lưu tự động
3. Khi quay lại, chế độ đã chọn sẽ được giữ nguyên

### Cho Developer

#### Toggle programmatically:
```javascript
// Bật dark mode
window.darkMode.enable();

// Tắt dark mode
window.darkMode.disable();

// Toggle
window.darkMode.toggle();

// Kiểm tra trạng thái
if (window.darkMode.isEnabled()) {
  console.log('Dark mode is on');
}
```

#### Thêm custom styles cho dark mode:
```css
/* Trong file CSS của bạn */
body.dark-mode .your-component {
  background-color: var(--dm-bg-card);
  color: var(--dm-text-primary);
}
```

## Color Variables

### Dark Mode Colors:
```css
--dm-bg-primary: #0d1117      /* Background chính */
--dm-bg-secondary: #161b22    /* Background phụ */
--dm-bg-tertiary: #1c2128     /* Background tertiary */
--dm-bg-card: #21262d         /* Card background */
--dm-bg-hover: #30363d        /* Hover state */

--dm-text-primary: #e6edf3    /* Text chính */
--dm-text-secondary: #8b949e  /* Text phụ */
--dm-text-muted: #6e7681      /* Text muted */

--dm-border: #30363d          /* Border color */
--dm-primary: #58a6ff         /* Primary color */
--dm-success: #3fb950         /* Success color */
--dm-warning: #d29922         /* Warning color */
--dm-danger: #f85149          /* Danger color */
```

## Tính Năng

### 1. Auto-detect System Preference
- Tự động phát hiện nếu OS đang dùng dark mode
- Chỉ áp dụng nếu user chưa set preference

### 2. LocalStorage Persistence
- Lưu trữ: `localStorage.setItem('darkMode', 'enabled')`
- Giữ nguyên preference qua các sessions

### 3. Smooth Transitions
- Tất cả elements có transition 0.3s
- Chuyển đổi mượt mà không giật lag

### 4. Comprehensive Coverage
Đã style cho:
- ✅ Navbar & Navigation
- ✅ Cards & Containers
- ✅ Forms & Inputs
- ✅ Tables
- ✅ Buttons
- ✅ Alerts & Toasts
- ✅ Modals
- ✅ Badges
- ✅ Footer
- ✅ Scrollbar
- ✅ Links
- ✅ Code blocks

## Testing

### Test Cases:
1. ✅ Click toggle button → Dark mode bật/tắt
2. ✅ Refresh page → Preference được giữ nguyên
3. ✅ Clear localStorage → Fallback về system preference
4. ✅ Change system theme → Auto update (nếu chưa set preference)
5. ✅ Navigate giữa các pages → Dark mode consistent

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

## Performance

- CSS file size: ~8KB
- JS file size: ~2KB
- No external dependencies
- Minimal performance impact

## Future Enhancements

Có thể thêm:
- [ ] Auto dark mode theo giờ (6PM - 6AM)
- [ ] Scheduled dark mode
- [ ] Multiple themes (not just dark/light)
- [ ] Custom color picker
- [ ] Sync across devices (requires backend)

## Troubleshooting

### Dark mode không hoạt động?
1. Kiểm tra console có lỗi không
2. Verify files đã load: dark-mode.css và dark-mode.js
3. Clear cache và reload

### Một số elements không đổi màu?
1. Thêm styles vào dark-mode.css
2. Sử dụng `body.dark-mode .your-selector`
3. Đảm bảo specificity đủ cao

### Toggle button không hiện?
1. Kiểm tra `id="darkModeToggle"` trong base.html
2. Verify CSS cho `.dark-mode-toggle` đã load

## Credits

Thiết kế lấy cảm hứng từ:
- GitHub Dark Theme
- Discord Dark Mode
- Modern UI/UX best practices
