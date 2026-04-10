/**
 * PWA Installation and Management
 * Handles service worker registration, install prompts, and offline detection
 */

let deferredPrompt;
let swRegistration;

// Initialize PWA features when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPWA);
} else {
  initPWA();
}

async function initPWA() {
  // Register service worker
  if ('serviceWorker' in navigator) {
    try {
      swRegistration = await navigator.serviceWorker.register('/sw.js');
      console.log('[PWA] Service Worker registered:', swRegistration);
      
      // Check for updates
      swRegistration.addEventListener('updatefound', () => {
        const newWorker = swRegistration.installing;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            showUpdateNotification();
          }
        });
      });
    } catch (error) {
      console.error('[PWA] Service Worker registration failed:', error);
    }
  }

  // Handle install prompt
  setupInstallPrompt();
  
  // Setup offline detection
  setupOfflineDetection();
  
  // Setup background sync
  setupBackgroundSync();
  
  // Check if already installed
  checkIfInstalled();
}

// Setup install prompt
function setupInstallPrompt() {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallButton();
  });

  window.addEventListener('appinstalled', () => {
    console.log('[PWA] App installed');
    deferredPrompt = null;
    hideInstallButton();
    showToast('Đã cài đặt ứng dụng thành công! 🎉', 'success');
  });
}

// Show install button
function showInstallButton() {
  const installBtn = document.getElementById('pwa-install-btn');
  if (installBtn) {
    installBtn.style.display = 'block';
    installBtn.addEventListener('click', promptInstall);
  } else {
    // Create floating install button
    createFloatingInstallButton();
  }
}

// Create floating install button
function createFloatingInstallButton() {
  const btn = document.createElement('button');
  btn.id = 'pwa-install-floating';
  btn.className = 'pwa-install-floating';
  btn.innerHTML = `
    <i class="bi bi-download"></i>
    <span>Cài đặt App</span>
  `;
  btn.addEventListener('click', promptInstall);
  document.body.appendChild(btn);
  
  // Auto hide after 10 seconds
  setTimeout(() => {
    btn.classList.add('hidden');
  }, 10000);
}

// Prompt install
async function promptInstall() {
  if (!deferredPrompt) {
    return;
  }

  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  console.log('[PWA] Install prompt outcome:', outcome);
  
  if (outcome === 'accepted') {
    hideInstallButton();
  }
  
  deferredPrompt = null;
}

// Hide install button
function hideInstallButton() {
  const installBtn = document.getElementById('pwa-install-btn');
  if (installBtn) {
    installBtn.style.display = 'none';
  }
  
  const floatingBtn = document.getElementById('pwa-install-floating');
  if (floatingBtn) {
    floatingBtn.remove();
  }
}

// Check if app is installed
function checkIfInstalled() {
  // Check if running in standalone mode
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                       window.navigator.standalone ||
                       document.referrer.includes('android-app://');
  
  if (isStandalone) {
    console.log('[PWA] Running in standalone mode');
    document.body.classList.add('pwa-installed');
    
    // Hide install button if exists
    hideInstallButton();
  }
}

// Setup offline detection
function setupOfflineDetection() {
  const updateOnlineStatus = async () => {
    const isOnline = navigator.onLine;
    document.body.classList.toggle('offline', !isOnline);
    
    if (!isOnline) {
      showOfflineBanner();
    } else {
      hideOfflineBanner();
      // Sync when back online
      if (swRegistration && swRegistration.active && 'sync' in swRegistration) {
        try {
          await swRegistration.sync.register('sync-exam-results');
        } catch (error) {
          console.log('[PWA] Background sync not available:', error);
        }
      }
    }
  };

  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  
  // Initial check
  updateOnlineStatus();
}

// Show offline banner
function showOfflineBanner() {
  let banner = document.getElementById('offline-banner');
  
  if (!banner) {
    banner = document.createElement('div');
    banner.id = 'offline-banner';
    banner.className = 'offline-banner';
    banner.innerHTML = `
      <i class="bi bi-wifi-off"></i>
      <span>Bạn đang offline. Một số tính năng có thể bị giới hạn.</span>
    `;
    document.body.prepend(banner);
  }
  
  banner.style.display = 'flex';
}

// Hide offline banner
function hideOfflineBanner() {
  const banner = document.getElementById('offline-banner');
  if (banner) {
    banner.style.display = 'none';
    showToast('Đã kết nối lại internet! ✓', 'success');
  }
}

// Show update notification
function showUpdateNotification() {
  const notification = document.createElement('div');
  notification.className = 'update-notification';
  notification.innerHTML = `
    <div class="update-content">
      <i class="bi bi-arrow-clockwise"></i>
      <span>Có phiên bản mới!</span>
    </div>
    <button onclick="updateApp()" class="btn btn-sm btn-primary">Cập nhật</button>
  `;
  document.body.appendChild(notification);
}

// Update app
window.updateApp = function() {
  if (swRegistration && swRegistration.waiting) {
    swRegistration.waiting.postMessage({ action: 'skipWaiting' });
    window.location.reload();
  }
};

// Setup background sync
function setupBackgroundSync() {
  if (swRegistration && swRegistration.active && 'sync' in swRegistration) {
    // Listen for form submissions to queue for sync
    document.addEventListener('submit', async (e) => {
      const form = e.target;
      
      // Only sync exam results and important forms
      if (form.classList.contains('sync-form') && !navigator.onLine) {
        e.preventDefault();
        
        try {
          // Save to IndexedDB
          const formData = new FormData(form);
          await saveToIndexedDB('pending-results', Object.fromEntries(formData));
          
          // Register sync
          await swRegistration.sync.register('sync-exam-results');
          
          showToast('Kết quả đã được lưu. Sẽ đồng bộ khi có mạng.', 'success');
        } catch (error) {
          console.error('[PWA] Background sync failed:', error);
          showToast('Không thể lưu kết quả offline', 'error');
        }
      }
    });
  }
}

// Save to IndexedDB
async function saveToIndexedDB(storeName, data) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('thptqg-db', 1);
    
    request.onerror = () => reject(request.error);
    
    request.onsuccess = () => {
      const db = request.result;
      const transaction = db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const addRequest = store.add({
        ...data,
        timestamp: Date.now()
      });
      
      addRequest.onsuccess = () => resolve(addRequest.result);
      addRequest.onerror = () => reject(addRequest.error);
    };
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains(storeName)) {
        db.createObjectStore(storeName, { keyPath: 'id', autoIncrement: true });
      }
    };
  });
}

// Request notification permission
async function requestNotificationPermission() {
  if ('Notification' in window && Notification.permission === 'default') {
    const permission = await Notification.requestPermission();
    console.log('[PWA] Notification permission:', permission);
    return permission === 'granted';
  }
  return Notification.permission === 'granted';
}

// Subscribe to push notifications
async function subscribeToPush() {
  if (!swRegistration) {
    console.error('[PWA] Service Worker not registered');
    return;
  }

  try {
    const subscription = await swRegistration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
    });
    
    // Send subscription to server
    await fetch('/api/push-subscribe/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(subscription)
    });
    
    console.log('[PWA] Push subscription successful');
  } catch (error) {
    console.error('[PWA] Push subscription failed:', error);
  }
}

// Helper function for VAPID key
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

// Add to home screen prompt for iOS
function showIOSInstallPrompt() {
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
  const isInStandaloneMode = ('standalone' in window.navigator) && (window.navigator.standalone);
  
  if (isIOS && !isInStandaloneMode) {
    const prompt = document.createElement('div');
    prompt.className = 'ios-install-prompt';
    prompt.innerHTML = `
      <div class="ios-prompt-content">
        <p>Cài đặt ứng dụng này trên iPhone:</p>
        <ol>
          <li>Nhấn nút <i class="bi bi-box-arrow-up"></i> Share</li>
          <li>Chọn "Add to Home Screen"</li>
        </ol>
        <button onclick="this.parentElement.parentElement.remove()">Đóng</button>
      </div>
    `;
    document.body.appendChild(prompt);
  }
}

// Export functions for global use
window.PWA = {
  requestNotificationPermission,
  subscribeToPush,
  updateApp,
  showIOSInstallPrompt
};
