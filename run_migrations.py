#!/usr/bin/env python
"""
Script to run Django migrations for the flashcard test functionality.
Run this script after activating your Django virtual environment.
"""

import os
import sys
import subprocess

def run_migrations():
    """Run Django migrations to create the new flashcard test tables."""
    try:
        # Run the migrate command
        print("Running Django migrations...")
        result = subprocess.run([
            sys.executable, "manage.py", "migrate"
        ], check=True, capture_output=True, text=True)
        
        print("Migration output:")
        print(result.stdout)
        
        if result.stderr:
            print("Migration warnings/errors:")
            print(result.stderr)
            
        print("\nMigrations completed successfully!")
        print("The FlashcardTest and FlashcardTestAnswer tables have been created.")
        
    except subprocess.CalledProcessError as e:
        print(f"Migration failed with error: {e}")
        print(f"Output: {e.output if hasattr(e, 'output') else 'No output'}")
        print(f"Error: {e.stderr if hasattr(e, 'stderr') else 'No error output'}")
        return False
    except FileNotFoundError:
        print("Error: manage.py not found. Make sure you're in the project root directory.")
        return False
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return False
        
    return True

if __name__ == "__main__":
    print("Preparing to run Django migrations for flashcard test functionality...")
    print("Make sure you have activated your virtual environment before running this script.")
    print(f"Using Python interpreter: {sys.executable}")
    print()
    
    success = run_migrations()
    
    if success:
        print("\nThe new FlashcardTest functionality should now be available.")
        print("You can access the test mode at: /kien-thuc/flashcard/<set_id>/test/")
    else:
        print("\nMigration failed. Please check the error messages above and try again.")
        print("Make sure Django is installed and your virtual environment is activated.")