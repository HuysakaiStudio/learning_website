#!/usr/bin/env python
"""
Migration Script for Adding Image Support to Questions

This script creates and runs the migration for adding image support to the CauHoi model.
Run this script after installing Django and dependencies.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def setup_django():
    """Initialize Django"""
    django.setup()

def create_and_run_migration():
    """Create and run the migration for image field"""
    try:
        setup_django()
        
        # Import Django management commands
        from django.core.management import execute_from_command_line
        
        # Create migration
        print("Creating migration for image field...")
        execute_from_command_line(['manage.py', 'makemigrations', 'de_thi'])
        
        # Run migration
        print("Running migration...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("Migration completed successfully!")
        
    except ImportError as e:
        print(f"Django not installed or not accessible: {e}")
        print("Please install Django first using: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    create_and_run_migration()