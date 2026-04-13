#!/usr/bin/env python
"""
Script to prepare and commit all changes to git, including handling deleted files
"""

def prepare_comprehensive_commit():
    """
    Prepare a comprehensive commit that includes all changes
    """
    
    print("=== Preparing Comprehensive Commit ===\n")
    
    print("IMPORTANT FILES THAT WERE DELETED (need attention):")
    print("- PYTHONANYWHERE_MIGRATION_FIX.md")
    print("- PYTHONANYWHERE_UPDATE_GUIDE.md") 
    print("- analyze_xp_system.py")
    print("- run_migrations.py")
    print()
    
    print("MODIFIED FILES (will be included in commit):")
    modified_files = [
        "apps/de_thi/forms.py",
        "apps/de_thi/views.py", 
        "apps/nguoi_dung/signals.py",
        "config/urls.py",
        "static/css/exam-results.css",
        "static/css/exam-taking.css", 
        "static/css/practice-mode.css",
        "templates/base.html",
        "templates/de_thi/chon_che_do.html",
        "templates/de_thi/danh_sach_de.html",
        "templates/de_thi/ket_qua.html",
        "templates/de_thi/lam_bai.html",
        "templates/de_thi/luyen_tung_cau.html",
        "templates/de_thi/sua_cau_hoi.html",
        "templates/de_thi/them_cau_hoi.html",
        "templates/de_thi/xem_dap_an.html",
        "templates/kien_thuc/flashcard_test.html",
        "templates/notifications/list.html",
        "templates/notifications/preferences.html",
        "templates/notifications/widget.html"
    ]
    
    for f in modified_files:
        print(f"  ~ {f}")
    print()
    
    print("NEW UNTRACKED FILES (will be included in commit):")
    new_files = [
        ".skills/",
        "IMAGE_SUPPORT_COMPLETE_DOCUMENTATION.md",
        "IMAGE_SUPPORT_IMPLEMENTATION.md",
        "IMAGE_SUPPORT_IMPLEMENTATION_SUMMARY.md",
        "apps/de_thi/migrations/0009_ketqua_danh_dau_khong_chinh_thuc.py",
        "apps/de_thi/migrations/0010_alter_cauhoi_options_cauhoi_hinh_anh.py",
        "apps/de_thi/migrations/0011_useranalytics_tong_bai_da_lam.py",
        "apps/de_thi/migrations/0013_test_migration_dependency.py",
        "check_image_field.py",
        "check_migration_state.py",
        "check_user_profiles.py",
        "commit_uncommitted_changes.py",
        "create_migration.py",
        "fix_pythonanywhere_migration.py",
        "lam_bai_view_patch.md",
        "pull_commits_guide.py",
        "verify_image_field.py"
    ]
    
    for f in new_files:
        print(f"  + {f}")
    print()
    
    print("=== CRITICAL MIGRATION FILES FOR PYTHONANYWHERE ===")
    print("These migration files are essential for fixing your server issue:")
    print("- apps/de_thi/migrations/0011_useranalytics_tong_bai_da_lam.py (the missing dependency)")
    print("- apps/de_thi/migrations/0010_alter_cauhoi_options_cauhoi_hinh_anh.py")
    print("- apps/de_thi/migrations/0009_ketqua_danh_dau_khong_chinh_thuc.py")
    print()
    
    print("=== COMMIT INSTRUCTIONS ===")
    print("1. Stage all changes (including new and modified files):")
    print("   git add .")
    print()
    
    print("2. If you want to recover deleted files before committing, run:")
    print("   git checkout HEAD -- PYTHONANYWHERE_MIGRATION_FIX.md PYTHONANYWHERE_UPDATE_GUIDE.md analyze_xp_system.py run_migrations.py")
    print("   (Only do this if you want to keep these files)")
    print()
    
    print("3. Or if you want to permanently remove them from the repository, stage the deletion:")
    print("   git add -A  # This stages all changes including deletions")
    print()
    
    print("4. Create a comprehensive commit:")
    print("   git commit -m 'Comprehensive update: Include migration fixes, feature enhancements, and documentation'")
    print()
    
    print("5. Push to remote repository:")
    print("   git push origin main")
    print()
    
    print("6. On PythonAnywhere server, pull the changes:")
    print("   git pull origin main")
    print()
    
    print("7. Run migrations on PythonAnywhere:")
    print("   python manage.py migrate")
    print()
    
    print("=== REMINDER ===")
    print("Make sure these migration files reach your PythonAnywhere server:")
    print("- apps/de_thi/migrations/0011_useranalytics_tong_bai_da_lam.py")
    print("- apps/de_thi/migrations/0012_useranalytics_tong_gio_hoc.py (already existed)")
    print("- apps/de_thi/migrations/0010_alter_cauhoi_options_cauhoi_hinh_anh.py")
    print()
    print("This will resolve your NodeNotFoundError on the server.")

if __name__ == '__main__':
    prepare_comprehensive_commit()