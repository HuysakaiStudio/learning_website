/**
 * Mobile Navbar Enhancement Script
 * Adds auto-hide on scroll and swipe gestures
 */

(function() {
  'use strict';

  let lastScrollTop = 0;
  let scrollThreshold = 10;
  let isScrolling;

  // Auto-hide navbar on scroll down
  function handleNavbarScroll() {
    if (window.innerWidth > 768) return; // Only on mobile

    const navbar = document.querySelector('.navbar');
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

    // Clear timeout
    window.clearTimeout(isScrolling);

    // Scrolling down
    if (currentScroll > lastScrollTop && currentScroll > scrollThreshold) {
      navbar.classList.add('navbar-hidden');
    } 
    // Scrolling up
    else if (currentScroll < lastScrollTop) {
      navbar.classList.remove('navbar-hidden');
    }

    // Compact navbar when scrolled
    if (currentScroll > 50) {
      navbar.classList.add('navbar-compact');
    } else {
      navbar.classList.remove('navbar-compact');
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;

    // Set a timeout to run after scrolling ends
    isScrolling = setTimeout(() => {
      navbar.classList.remove('navbar-hidden');
    }, 150);
  }

  // Swipe to close menu
  function setupSwipeGestures() {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (!navbarCollapse) return;

    let touchStartX = 0;
    let touchEndX = 0;

    navbarCollapse.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    navbarCollapse.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }, { passive: true });

    function handleSwipe() {
      const swipeDistance = touchEndX - touchStartX;
      
      // Swipe left to close (at least 100px)
      if (swipeDistance < -100) {
        const navbarToggler = document.querySelector('.navbar-toggler');
        if (navbarToggler && navbarToggler.getAttribute('aria-expanded') === 'true') {
          navbarToggler.click();
        }
      }
    }
  }

  // Close menu when clicking outside
  function setupClickOutside() {
    document.addEventListener('click', (e) => {
      const navbar = document.querySelector('.navbar');
      const navbarCollapse = document.querySelector('.navbar-collapse');
      const navbarToggler = document.querySelector('.navbar-toggler');

      if (!navbar.contains(e.target) && navbarCollapse.classList.contains('show')) {
        navbarToggler.click();
      }
    });
  }

  // Active link highlighting
  function highlightActiveLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link, .mobile-bottom-nav a');

    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }

  // Create bottom navigation
  function createBottomNav() {
    if (window.innerWidth > 768) return;

    // Check if already exists
    if (document.querySelector('.mobile-bottom-nav')) return;

    const bottomNav = document.createElement('nav');
    bottomNav.className = 'mobile-bottom-nav';
    bottomNav.innerHTML = `
      <a href="/" class="bottom-nav-item">
        <i class="bi bi-house-fill"></i>
        <span>Trang chủ</span>
      </a>
      <a href="/de-thi/" class="bottom-nav-item">
        <i class="bi bi-file-text-fill"></i>
        <span>Đề thi</span>
      </a>
      <a href="/kien-thuc/flashcard/" class="bottom-nav-item">
        <i class="bi bi-lightbulb-fill"></i>
        <span>Flashcard</span>
      </a>
      <a href="/leaderboard/" class="bottom-nav-item">
        <i class="bi bi-trophy-fill"></i>
        <span>Xếp hạng</span>
      </a>
      <a href="/nguoi-dung/profile/" class="bottom-nav-item">
        <i class="bi bi-person-fill"></i>
        <span>Cá nhân</span>
      </a>
    `;

    document.body.appendChild(bottomNav);
    highlightActiveLink();
  }

  // Haptic feedback (if supported)
  function hapticFeedback() {
    if ('vibrate' in navigator) {
      navigator.vibrate(10);
    }
  }

  // Add haptic to all clickable elements
  function setupHapticFeedback() {
    const clickables = document.querySelectorAll('.nav-link, .btn, .mobile-bottom-nav a');
    clickables.forEach(el => {
      el.addEventListener('click', hapticFeedback, { passive: true });
    });
  }

  // Initialize
  function init() {
    // Only run on mobile
    if (window.innerWidth <= 768) {
      window.addEventListener('scroll', handleNavbarScroll, { passive: true });
      setupSwipeGestures();
      setupClickOutside();
      createBottomNav();
      setupHapticFeedback();
      highlightActiveLink();
    }

    // Re-init on resize
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (window.innerWidth <= 768) {
          createBottomNav();
        } else {
          const bottomNav = document.querySelector('.mobile-bottom-nav');
          if (bottomNav) bottomNav.remove();
        }
      }, 250);
    });
  }

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
