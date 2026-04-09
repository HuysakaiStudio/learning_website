/**
 * Psychology-Based UX Enhancements
 * Implements cognitive science principles for better user experience
 */

// ============================================
// MICRO-INTERACTIONS
// ============================================

class MicroInteractions {
  constructor() {
    this.init();
  }

  init() {
    this.setupButtonFeedback();
    this.setupCardHoverEffects();
    this.setupFormValidation();
    this.setupProgressAnimations();
  }

  // Button click feedback with haptic-like animation
  setupButtonFeedback() {
    document.addEventListener('click', (e) => {
      const button = e.target.closest('button, .btn, a.btn');
      if (button && !button.disabled) {
        this.createRipple(e, button);
      }
    });
  }

  createRipple(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.5);
      left: ${x}px;
      top: ${y}px;
      pointer-events: none;
      transform: scale(0);
      animation: ripple 0.6s ease-out;
    `;

    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  }

  // Card hover effects with depth perception
  setupCardHoverEffects() {
    const cards = document.querySelectorAll('.card, .feature-tile, .card-psychology');
    
    cards.forEach(card => {
      card.addEventListener('mouseenter', (e) => {
        this.addCardDepth(card);
      });
      
      card.addEventListener('mouseleave', (e) => {
        this.removeCardDepth(card);
      });
    });
  }

  addCardDepth(card) {
    card.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    card.style.transform = 'translateY(-8px) scale(1.02)';
  }

  removeCardDepth(card) {
    card.style.transform = 'translateY(0) scale(1)';
  }

  // Real-time form validation with positive feedback
  setupFormValidation() {
    const inputs = document.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
      input.addEventListener('blur', () => {
        this.validateInput(input);
      });
      
      input.addEventListener('input', () => {
        if (input.classList.contains('is-invalid')) {
          this.validateInput(input);
        }
      });
    });
  }

  validateInput(input) {
    if (input.checkValidity()) {
      input.classList.remove('is-invalid');
      input.classList.add('is-valid');
      this.showSuccessIcon(input);
    } else {
      input.classList.remove('is-valid');
      input.classList.add('is-invalid');
    }
  }

  showSuccessIcon(input) {
    const icon = document.createElement('i');
    icon.className = 'bi bi-check-circle-fill text-success';
    icon.style.cssText = 'position: absolute; right: 10px; top: 50%; transform: translateY(-50%);';
    
    const wrapper = input.parentElement;
    if (wrapper.style.position !== 'relative') {
      wrapper.style.position = 'relative';
    }
    
    const existingIcon = wrapper.querySelector('.bi-check-circle-fill');
    if (existingIcon) existingIcon.remove();
    
    wrapper.appendChild(icon);
  }

  // Animated progress bars
  setupProgressAnimations() {
    const progressBars = document.querySelectorAll('.progress-psychology-fill, .progress-bar');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateProgress(entry.target);
        }
      });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => observer.observe(bar));
  }

  animateProgress(bar) {
    const targetWidth = bar.style.width || bar.getAttribute('data-width') || '0%';
    bar.style.width = '0%';
    
    setTimeout(() => {
      bar.style.transition = 'width 1s cubic-bezier(0.4, 0, 0.2, 1)';
      bar.style.width = targetWidth;
    }, 100);
  }
}

// ============================================
// GAMIFICATION SYSTEM
// ============================================

class GamificationSystem {
  constructor() {
    // Initialize with default values - will be loaded from server
    this.xp = 0;
    this.level = 0;
    this.streak = 0;
    this.lastStudyDate = null;
    this.syncing = false;
    this.serverLoaded = false;
    this.init();
  }

  init() {
    this.loadFromServer();
  }

  async loadFromServer() {
    try {
      const response = await fetch('/nguoi-dung/api/gamification/stats/');
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Update from server - server is source of truth
          this.xp = data.data.xp;
          this.level = data.data.level;
          this.streak = data.data.current_streak;
          this.serverLoaded = true;
          
          // Update localStorage as cache only (read-only for display)
          localStorage.setItem('userXP', this.xp);
          localStorage.setItem('studyStreak', this.streak);
          
          this.updateDisplay();
          
          // One-time migration from old localStorage data
          await this.migrateOldData();
        }
      }
    } catch (error) {
      console.log('Server unavailable, using cached data');
      // Fallback to localStorage cache for offline display only
      this.xp = parseInt(localStorage.getItem('userXP')) || 0;
      this.level = this.calculateLevel(this.xp);
      this.streak = parseInt(localStorage.getItem('studyStreak')) || 0;
      this.updateDisplay();
    }
  }

  async migrateOldData() {
    // One-time migration: if localStorage has more data, sync it to server
    const localXP = parseInt(localStorage.getItem('userXP')) || 0;
    const localStreak = parseInt(localStorage.getItem('studyStreak')) || 0;
    
    if (localXP > this.xp || localStreak > this.streak) {
      try {
        const response = await fetch('/nguoi-dung/api/gamification/sync/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            xp: localXP,
            streak: localStreak
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            this.xp = data.data.xp;
            this.level = data.data.level;
            this.streak = data.data.current_streak;
            localStorage.setItem('userXP', this.xp);
            localStorage.setItem('studyStreak', this.streak);
            this.updateDisplay();
            console.log('Old data migrated successfully');
          }
        }
      } catch (error) {
        console.log('Migration failed, will retry later');
      }
    }
  }

  calculateLevel(xp) {
    return Math.floor(Math.pow(xp / 100, 1 / 1.5));
  }

  async addXP(amount, reason = '') {
    this.xp += amount;
    const newLevel = this.calculateLevel(this.xp);
    
    localStorage.setItem('userXP', this.xp);
    
    // Show XP gain notification
    this.showXPNotification(amount, reason);
    
    // Check for level up
    if (newLevel > this.level) {
      this.level = newLevel;
      this.showLevelUpNotification(newLevel);
    }
    
    this.updateDisplay();
    
    // Sync to server
    this.syncXPToServer(amount, reason);
  }

  async syncXPToServer(amount, reason) {
    if (this.syncing) return;
    
    try {
      this.syncing = true;
      const response = await fetch('/nguoi-dung/api/gamification/add-xp/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: amount,
          reason: reason
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Update from server response
          this.xp = data.data.total_xp;
          this.level = data.data.new_level;
          localStorage.setItem('userXP', this.xp);
          this.updateDisplay();
        }
      }
    } catch (error) {
      console.log('XP sync failed, saved locally');
    } finally {
      this.syncing = false;
    }
  }

  showXPNotification(amount, reason) {
    const notification = document.createElement('div');
    notification.className = 'xp-notification';
    notification.innerHTML = `
      <div class="xp-gain">
        <i class="bi bi-star-fill"></i>
        <span>+${amount} XP</span>
        ${reason ? `<small>${reason}</small>` : ''}
      </div>
    `;
    
    notification.style.cssText = `
      position: fixed;
      top: 80px;
      right: 20px;
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      color: white;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3);
      z-index: 9999;
      animation: slideInRight 0.5s ease-out, fadeOut 0.5s ease-out 2.5s;
    `;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
  }

  showLevelUpNotification(level) {
    const modal = document.createElement('div');
    modal.className = 'level-up-modal';
    modal.innerHTML = `
      <div class="level-up-content">
        <div class="level-up-animation">
          <i class="bi bi-trophy-fill"></i>
        </div>
        <h2>Level Up!</h2>
        <p class="level-number">Level ${level}</p>
        <p class="level-message">Bạn đã đạt cấp độ mới! Tiếp tục phát huy!</p>
        <button class="btn btn-primary" onclick="this.closest('.level-up-modal').remove()">
          Tuyệt vời! 🎉
        </button>
      </div>
    `;
    
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      animation: fadeIn 0.3s ease-out;
    `;
    
    document.body.appendChild(modal);
  }

  async checkStreak() {
    // Streak is now managed by server only
    // Call server to update streak
    try {
      const response = await fetch('/nguoi-dung/api/gamification/update-streak/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          const oldStreak = this.streak;
          this.streak = data.data.current_streak;
          
          // Update localStorage cache
          localStorage.setItem('studyStreak', this.streak);
          this.updateDisplay();
          
          // Check for streak milestones
          if ([3, 7, 30, 100].includes(this.streak) && this.streak > oldStreak) {
            this.showStreakMilestone(this.streak);
          }
        }
      }
    } catch (error) {
      console.log('Streak update failed - server unavailable');
    }
  }

  showStreakMilestone(days) {
    const rewards = {
      3: { bonus: 10, message: '3 ngày liên tiếp! 🔥' },
      7: { bonus: 30, message: '1 tuần hoàn hảo! ⭐' },
      30: { bonus: 200, message: '1 tháng kiên trì! 🏆' },
      100: { bonus: 1000, message: '100 ngày huyền thoại! 👑' }
    };
    
    const reward = rewards[days];
    if (reward) {
      this.addXP(reward.bonus, reward.message);
    }
  }

  showStreakLostNotification() {
    this.showToast('Chuỗi học tập đã bị gián đoạn. Hãy bắt đầu lại! 💪', 'warning');
  }

  updateDisplay() {
    // Update XP display if element exists
    const xpDisplay = document.getElementById('user-xp');
    if (xpDisplay) {
      xpDisplay.textContent = `${this.xp} XP`;
    }
    
    // Update level display
    const levelDisplay = document.getElementById('user-level');
    if (levelDisplay) {
      levelDisplay.textContent = `Level ${this.level}`;
    }
    
    // Update streak display
    const streakDisplay = document.getElementById('study-streak');
    if (streakDisplay) {
      streakDisplay.innerHTML = `<span class="streak-fire">🔥</span> ${this.streak} ngày`;
    }
  }

  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    const container = document.getElementById('toast-container') || document.body;
    container.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
  }
}

// ============================================
// FOCUS MODE
// ============================================

class FocusMode {
  constructor() {
    this.isActive = false;
    this.pomodoroTimer = null;
    this.workDuration = 25 * 60; // 25 minutes
    this.breakDuration = 5 * 60; // 5 minutes
    this.timeRemaining = this.workDuration;
  }

  toggle() {
    this.isActive = !this.isActive;
    
    if (this.isActive) {
      this.activate();
    } else {
      this.deactivate();
    }
  }

  activate() {
    // Hide distractions
    document.querySelectorAll('.hide-in-focus').forEach(el => {
      el.style.display = 'none';
    });
    
    // Show focus overlay
    const overlay = document.createElement('div');
    overlay.id = 'focus-mode-overlay';
    overlay.className = 'focus-mode-active';
    overlay.innerHTML = `
      <div class="focus-mode-panel">
        <h3>Chế độ tập trung</h3>
        <div class="pomodoro-timer">
          <div class="timer-display">${this.formatTime(this.timeRemaining)}</div>
          <button class="btn btn-primary" onclick="focusMode.startPomodoro()">
            Bắt đầu
          </button>
        </div>
        <button class="btn btn-outline-primary" onclick="focusMode.toggle()">
          Thoát chế độ tập trung
        </button>
      </div>
    `;
    
    document.body.appendChild(overlay);
  }

  deactivate() {
    // Show hidden elements
    document.querySelectorAll('.hide-in-focus').forEach(el => {
      el.style.display = '';
    });
    
    // Remove overlay
    const overlay = document.getElementById('focus-mode-overlay');
    if (overlay) overlay.remove();
    
    // Stop timer
    if (this.pomodoroTimer) {
      clearInterval(this.pomodoroTimer);
      this.pomodoroTimer = null;
    }
  }

  startPomodoro() {
    this.timeRemaining = this.workDuration;
    
    this.pomodoroTimer = setInterval(() => {
      this.timeRemaining--;
      
      const display = document.querySelector('.timer-display');
      if (display) {
        display.textContent = this.formatTime(this.timeRemaining);
      }
      
      if (this.timeRemaining <= 0) {
        this.pomodoroComplete();
      }
    }, 1000);
  }

  pomodoroComplete() {
    clearInterval(this.pomodoroTimer);
    
    // Play notification sound (if available)
    this.playNotificationSound();
    
    // Show completion message
    alert('Pomodoro hoàn thành! Hãy nghỉ ngơi 5 phút. 🎉');
    
    // Award XP
    if (window.gamification) {
      window.gamification.addXP(20, 'Hoàn thành Pomodoro');
    }
  }

  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  playNotificationSound() {
    // Simple beep using Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
  }
}

// ============================================
// COGNITIVE LOAD HELPERS
// ============================================

class CognitiveLoadManager {
  constructor() {
    this.init();
  }

  init() {
    this.setupProgressiveDisclosure();
    this.setupSkeletonLoaders();
    this.setupLazyLoading();
  }

  // Progressive disclosure - show more details on demand
  setupProgressiveDisclosure() {
    document.querySelectorAll('[data-toggle="details"]').forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = trigger.getAttribute('data-target');
        const target = document.getElementById(targetId);
        
        if (target) {
          target.classList.toggle('hidden');
          trigger.textContent = target.classList.contains('hidden') 
            ? 'Xem thêm ▼' 
            : 'Thu gọn ▲';
        }
      });
    });
  }

  // Skeleton loaders for better perceived performance
  setupSkeletonLoaders() {
    document.querySelectorAll('[data-skeleton]').forEach(element => {
      this.showSkeleton(element);
      
      // Simulate loading (replace with actual data loading)
      setTimeout(() => {
        this.hideSkeleton(element);
      }, 1000);
    });
  }

  showSkeleton(element) {
    element.classList.add('skeleton');
    element.setAttribute('aria-busy', 'true');
  }

  hideSkeleton(element) {
    element.classList.remove('skeleton');
    element.removeAttribute('aria-busy');
  }

  // Lazy loading for images and heavy content
  setupLazyLoading() {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove('lazy');
          imageObserver.unobserve(img);
        }
      });
    });

    document.querySelectorAll('img.lazy').forEach(img => {
      imageObserver.observe(img);
    });
  }
}

// ============================================
// INITIALIZATION
// ============================================

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Initialize micro-interactions
  window.microInteractions = new MicroInteractions();
  
  // Initialize gamification
  window.gamification = new GamificationSystem();
  
  // Initialize focus mode
  window.focusMode = new FocusMode();
  
  // Initialize cognitive load manager
  window.cognitiveLoad = new CognitiveLoadManager();
  
  // Add CSS animations
  addAnimationStyles();
  
  console.log('🧠 Psychology-based UX enhancements loaded');
});

// Add required CSS animations
function addAnimationStyles() {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes ripple {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }
    
    @keyframes slideInRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    @keyframes fadeOut {
      to {
        opacity: 0;
        transform: translateY(-20px);
      }
    }
    
    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
    
    .level-up-content {
      background: white;
      padding: 3rem;
      border-radius: 1.5rem;
      text-align: center;
      max-width: 400px;
      animation: achievement-unlock 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .level-up-animation i {
      font-size: 5rem;
      color: #fbbf24;
      animation: pulse 1s infinite;
    }
    
    .level-number {
      font-size: 3rem;
      font-weight: 800;
      color: #2563eb;
      margin: 1rem 0;
    }
    
    .focus-mode-panel {
      background: white;
      padding: 2rem;
      border-radius: 1.5rem;
      text-align: center;
      min-width: 300px;
    }
    
    .timer-display {
      font-size: 3rem;
      font-weight: 700;
      color: #2563eb;
      margin: 1.5rem 0;
      font-family: 'Courier New', monospace;
    }
  `;
  
  document.head.appendChild(style);
}

// Export for use in other scripts
window.PsychologyUX = {
  MicroInteractions,
  GamificationSystem,
  FocusMode,
  CognitiveLoadManager
};
