#!/usr/bin/env python
"""
Guide for pulling commits to PythonAnywhere server
"""

def guide_pull_commits():
    """
    Comprehensive guide to pull commits to PythonAnywhere server
    """
    
    print("=== How to Pull Commits to PythonAnywhere Server ===\n")
    
    print("Method 1: Direct Git Pull (Recommended)")
    print("---------------------------------------")
    print("1. Log in to your PythonAnywhere console")
    print("2. Navigate to your project directory:")
    print("   $ cd ~/your_project_directory")
    print("3. Pull the latest changes:")
    print("   $ git pull origin main")
    print("   (or 'master' if that's your default branch)\n")
    
    print("Method 2: If you have uncommitted changes on the server")
    print("-----------------------------------------------------")
    print("1. Stash your server changes (if any):")
    print("   $ git stash")
    print("2. Pull the latest changes:")
    print("   $ git pull origin main")
    print("3. Reapply stashed changes (if needed):")
    print("   $ git stash pop\n")
    
    print("Method 3: If you get merge conflicts")
    print("------------------------------------")
    print("1. Check the status:")
    print("   $ git status")
    print("2. Resolve conflicts manually if any, then:")
    print("   $ git add .")
    print("   $ git commit -m 'Resolve merge conflicts'")
    print("3. Pull again:")
    print("   $ git pull origin main\n")
    
    print("Method 4: Hard reset to remote (CAUTION: This will erase local changes)")
    print("---------------------------------------------------------------------")
    print("1. Fetch the latest changes:")
    print("   $ git fetch origin")
    print("2. Reset to match remote:")
    print("   $ git reset --hard origin/main\n")
    
    print("Method 5: Clone fresh copy if needed")
    print("------------------------------------")
    print("1. Backup your current directory (optional but recommended):")
    print("   $ cd ~")
    print("   $ cp -r your_project_directory your_project_directory_backup")
    print("2. Remove old directory:")
    print("   $ rm -rf your_project_directory")
    print("3. Clone fresh copy:")
    print("   $ git clone https://github.com/yourusername/yourrepository.git your_project_directory\n")
    
    print("After pulling, remember to run:")
    print("----------------------------")
    print("1. Install/update requirements if requirements.txt changed:")
    print("   $ pip3 install -r requirements.txt")
    print("2. Run migrations:")
    print("   $ python3 manage.py migrate")
    print("3. Collect static files if needed:")
    print("   $ python3 manage.py collectstatic --noinput\n")
    
    print("Troubleshooting Tips:")
    print("---------------------")
    print("• If git pull fails, check your internet connection on the server")
    print("• If you get permission errors, make sure your SSH keys are set up correctly")
    print("• If you have credential issues, you may need to set up a personal access token")
    print("• Check which branch you're on: $ git branch")
    print("• Check remote URL: $ git remote -v\n")

if __name__ == '__main__':
    guide_pull_commits()