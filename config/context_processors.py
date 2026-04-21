import os
from pathlib import Path
from django.conf import settings

def cache_buster(request):
    """Add cache version to all templates based on static files modification time"""
    # Lấy thời gian sửa đổi mới nhất của các file CSS chính
    static_dir = settings.BASE_DIR / 'static' / 'css'

    try:
        if static_dir.exists():
            # Lấy mtime mới nhất của tất cả file CSS
            css_files = list(static_dir.glob('*.css'))
            if css_files:
                latest_mtime = max(os.path.getmtime(f) for f in css_files)
                cache_version = int(latest_mtime)
            else:
                cache_version = 1
        else:
            cache_version = 1
    except Exception:
        # Fallback nếu có lỗi
        cache_version = 1

    return {
        'CACHE_VERSION': cache_version
    }


def notebook_context(request):
    """Add notebook sidebar availability to all templates"""
    # Check if user is authenticated to determine if notebook sidebar should be available
    is_authenticated = hasattr(request, 'user') and request.user.is_authenticated
    
    return {
        'SHOW_NOTEBOOK_SIDEBAR': is_authenticated
    }
