#!/usr/bin/env python
"""
Script to help commit all uncommitted changes to git
"""

import subprocess
import os

def get_git_status():
    """Get current git status"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git not installed")
        return []

def categorize_changes(status_lines):
    """Categorize git changes"""
    added = []
    modified = []
    deleted = []
    untracked = []
    
    for line in status_lines:
        if line.startswith('A '):  # Added
            added.append(line[3:])
        elif line.startswith('M '):  # Modified
            modified.append(line[3:])
        elif line.startswith('D '):  # Deleted
            deleted.append(line[3:])
        elif line.startswith('??'):  # Untracked
            untracked.append(line[3:])
    
    return added, modified, deleted, untracked

def print_summary(added, modified, deleted, untracked):
    """Print summary of changes"""
    print("=== Git Changes Summary ===\n")
    
    if added:
        print(f"Added files ({len(added)}):")
        for f in added:
            print(f"  + {f}")
        print()
    
    if modified:
        print(f"Modified files ({len(modified)}):")
        for f in modified:
            print(f"  ~ {f}")
        print()
    
    if deleted:
        print(f"Deleted files ({len(deleted)}):")
        for f in deleted:
            print(f"  - {f}")
        print()
    
    if untracked:
        print(f"Untracked files ({len(untracked)}):")
        for f in untracked:
            print(f"  ? {f}")
        print()

def commit_all_changes():
    """Commit all changes with a comprehensive commit message"""
    print("Preparing to commit all changes...\n")
    
    status_lines = get_git_status()
    if not status_lines or status_lines == ['']:
        print("No changes to commit.")
        return
    
    added, modified, deleted, untracked = categorize_changes(status_lines)
    print_summary(added, modified, deleted, untracked)
    
    print("=== Recommended Commit Process ===")
    print("1. Adding all changes to staging area...")
    print("   git add .")
    print()
    
    print("2. Creating a comprehensive commit message")
    print("   git commit -m 'Sync: Update project with recent changes'")
    print()
    
    print("3. Pushing to remote repository")
    print("   git push origin main")
    print()
    
    print("=== Detailed Breakdown ===")
    print("The following changes will be committed:")
    
    total_changes = len(added) + len(modified) + len(deleted) + len(untracked)
    print(f"Total files affected: {total_changes}")
    
    if modified:
        print(f"- {len(modified)} modified files (bug fixes, feature additions, improvements)")
    if added:
        print(f"- {len(added)} new files (features, utilities, documentation)")
    if untracked:
        print(f"- {len(untracked)} previously untracked files (new functionality)")
    if deleted:
        print(f"- {len(deleted)} deleted files (cleanup, refactoring)")
    
    print("\n=== Important Migration Files ===")
    migration_files = [f for f in (added + modified + untracked) if 'migrations' in f and '.py' in f]
    if migration_files:
        print("Migration files that need to be on server:")
        for f in migration_files:
            print(f"  * {f}")
    
    print("\n=== Action Required ===")
    print("Run these commands in order:")
    print("1. git add .")
    print("2. git commit -m 'Sync: Update project with recent changes including migration fixes'")
    print("3. git push origin main")
    print("4. Then on PythonAnywhere: git pull origin main")

if __name__ == '__main__':
    commit_all_changes()