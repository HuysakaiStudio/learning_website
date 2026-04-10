/**
 * Dark Mode Toggle System
 * Lưu trữ preference trong localStorage và tự động áp dụng
 */

(function() {
  'use strict';

  const DARK_MODE_KEY = 'darkMode';
  const DARK_MODE_CLASS = 'dark-mode';

  // Khởi tạo dark mode từ localStorage hoặc system preference
  function initDarkMode() {
    const savedMode = localStorage.getItem(DARK_MODE_KEY);
    
    if (savedMode === 'enabled') {
      enableDarkMode();
    } else if (savedMode === 'disabled') {
      disableDarkMode();
    } else {
      // Kiểm tra system preference
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        enableDarkMode();
      }
    }
  }

  // Bật dark mode
  function enableDarkMode() {
    document.body.classList.add(DARK_MODE_CLASS);
    localStorage.setItem(DARK_MODE_KEY, 'enabled');
    updateToggleButton(true);
  }

  // Tắt dark mode
  function disableDarkMode() {
    document.body.classList.remove(DARK_MODE_CLASS);
    localStorage.setItem(DARK_MODE_KEY, 'disabled');
    updateToggleButton(false);
  }

  // Toggle dark mode
  function toggleDarkMode() {
    if (document.body.classList.contains(DARK_MODE_CLASS)) {
      disableDarkMode();
    } else {
      enableDarkMode();
    }
  }

  // Cập nhật trạng thái nút toggle
  function updateToggleButton(isDark) {
    const toggleBtns = [
      document.getElementById('theme-toggle'),
      document.getElementById('theme-toggle-mobile')
    ];

    toggleBtns.forEach(btn => {
      if (btn) {
        btn.setAttribute('aria-pressed', isDark);
        btn.title = isDark ? 'Chuyển sang chế độ sáng' : 'Chuyển sang chế độ tối';

        // Cập nhật icon
        const icon = btn.querySelector('i');
        if (icon) {
          icon.className = isDark ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        }
      }
    });
  }

  // Lắng nghe thay đổi system preference
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      const savedMode = localStorage.getItem(DARK_MODE_KEY);
      // Chỉ tự động thay đổi nếu user chưa set preference
      if (!savedMode) {
        if (e.matches) {
          enableDarkMode();
        } else {
          disableDarkMode();
        }
      }
    });
  }

  // Export functions để có thể gọi từ bên ngoài
  window.darkMode = {
    toggle: toggleDarkMode,
    enable: enableDarkMode,
    disable: disableDarkMode,
    isEnabled: () => document.body.classList.contains(DARK_MODE_CLASS)
  };

  // Khởi tạo khi DOM ready - chỉ chạy 1 lần
  document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo dark mode
    initDarkMode();

    // Gắn event listener cho cả 2 nút
    const toggleBtns = [
      document.getElementById('theme-toggle'),
      document.getElementById('theme-toggle-mobile')
    ];

    toggleBtns.forEach(btn => {
      if (btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          toggleDarkMode();
        });
      }
    });
  });

})();
