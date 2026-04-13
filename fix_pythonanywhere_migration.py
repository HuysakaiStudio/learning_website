#!/usr/bin/env python
"""
Script to fix the migration dependency issue on PythonAnywhere server
"""

def fix_migration_issue():
    """
    Instructions to fix the Django migration dependency issue on PythonAnywhere:
    
    The error 'NodeNotFoundError: Migration de_thi.0012_useranalytics_tong_gio_hoc 
    dependencies reference nonexistent parent node ('de_thi', '0011_useranalytics_tong_bai_da_lam')'
    occurs when migration files are missing from the server.
    """
    
    print("=== Fix for Django Migration Dependency Issue on PythonAnywhere ===\n")
    
    print("Problem:")
    print("- Migration 0012 depends on 0011, but 0011 is missing from the server")
    print("- This typically happens when files aren't properly synced to PythonAnywhere\n")
    
    print("Solution Steps:")
    print("1. Upload all migration files to your PythonAnywhere server")
    print("2. Make sure apps/de_thi/migrations/0011_useranalytics_tong_bai_da_lam.py exists on the server")
    print("3. Check that all migration files are present in the right location\n")
    
    print("To verify files are present on PythonAnywhere:")
    print("$ ls -la ~/your_project_directory/apps/de_thi/migrations/\n")
    
    print("If files are missing, you can either:")
    print("A) Upload the missing migration files via PythonAnywhere's Files tab")
    print("B) Or use git to sync your changes:")
    print("   - Commit your migration files locally: git add . && git commit -m 'Add missing migrations'")
    print("   - Push to your remote repo: git push origin main")
    print("   - Pull on PythonAnywhere: cd ~/your_project_directory && git pull origin main\n")
    
    print("Alternative solution - Fake the missing migration (only if files are on server but DB is wrong):")
    print("$ python manage.py migrate de_thi 0011 --fake")
    print("$ python manage.py migrate de_thi\n")
    
    print("If the migration files are already on the server but the dependency is still wrong:")
    print("1. Check if 0011_useranalytics_tong_bai_da_lam.py exists in apps/de_thi/migrations/")
    print("2. Verify its content has the correct dependencies")
    print("3. If needed, recreate the migration:\n")
    print("   $ python manage.py migrate --fake de_thi 0011  # if migration was already applied")
    print("   $ python manage.py migrate de_thi 0012")

if __name__ == '__main__':
    fix_migration_issue()