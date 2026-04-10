function showToast(message, type = 'error') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerText = message;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Mega Menu Keyboard Navigation and Accessibility
document.addEventListener('DOMContentLoaded', function() {
  // Initialize mega menus
  const megaDropdowns = document.querySelectorAll('.mega-dropdown');
  
  megaDropdowns.forEach(dropdown => {
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.mega-menu');
    
    if (!toggle || !menu) return;
    
    // Add ARIA attributes
    toggle.setAttribute('aria-haspopup', 'true');
    toggle.setAttribute('aria-expanded', 'false');
    menu.setAttribute('role', 'menu');
    
    // Handle keyboard navigation
    toggle.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      } else if (e.key === 'Escape') {
        this.parentElement.classList.remove('show');
        this.setAttribute('aria-expanded', 'false');
        this.focus();
      }
    });
    
    // Handle mouse events
    dropdown.addEventListener('mouseenter', function() {
      // Clear any existing timeouts to prevent accidental closing
      if (this.closeTimer) {
        clearTimeout(this.closeTimer);
        this.closeTimer = null;
      }
      
      // Show the menu after a short delay to prevent accidental triggers
      if (!this.classList.contains('show')) {
        this.showTimer = setTimeout(() => {
          this.classList.add('show');
          toggle.setAttribute('aria-expanded', 'true');
        }, 150);
      }
    });
    
    dropdown.addEventListener('mouseleave', function() {
      // Close the menu after a delay to allow for movement to the menu
      if (this.showTimer) {
        clearTimeout(this.showTimer);
        this.showTimer = null;
      }
      
      this.closeTimer = setTimeout(() => {
        this.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
      }, 300);
    });
    
    // Handle clicks on menu items
    const menuLinks = menu.querySelectorAll('.mega-link');
    menuLinks.forEach(link => {
      link.setAttribute('role', 'menuitem');
      link.setAttribute('tabindex', '-1'); // Will be focused programmatically
      
      link.addEventListener('click', function() {
        // Close the menu after clicking a link
        dropdown.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
    
    // Handle focus management within the menu
    menu.addEventListener('keydown', function(e) {
      const currentFocus = document.activeElement;
      const allFocusableElements = menu.querySelectorAll(
        'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      
      if (allFocusableElements.length === 0) return;
      
      const firstElement = allFocusableElements[0];
      const lastElement = allFocusableElements[allFocusableElements.length - 1];
      
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          // Shift + Tab: go backwards
          if (currentFocus === firstElement) {
            toggle.focus();
            e.preventDefault();
          }
        } else {
          // Tab: go forwards
          if (currentFocus === lastElement) {
            toggle.focus();
            e.preventDefault();
          }
        }
      } else if (e.key === 'Escape') {
        dropdown.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        // Focus the first item in the menu
        firstElement.focus();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        // Focus the last item in the menu
        lastElement.focus();
      }
    });
  });
  
  // Close all mega menus when clicking outside
  document.addEventListener('click', function(e) {
    megaDropdowns.forEach(dropdown => {
      const toggle = dropdown.querySelector('.dropdown-toggle');
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove('show');
        if (toggle) {
          toggle.setAttribute('aria-expanded', 'false');
        }
      }
    });
  });
});
