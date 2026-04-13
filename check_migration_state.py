#!/usr/bin/env python
"""
Script to check and fix the migration dependency issue for de_thi app
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from django.db.migrations.loader import MigrationLoader
from django.apps import apps

def check_migration_state():
    """Check the current migration state"""
    print("=== Checking Migration State ===")
    
    # Get migration loader
    loader = MigrationLoader(connection)
    
    # Check the de_thi app specifically
    de_thi_migrations = []
    for app_tuple, migration_obj in loader.disk_migrations.items():
        app_label, migration_name = app_tuple
        if app_label == 'de_thi':
            de_thi_migrations.append(migration_name)
        
    print(f"Disk migrations in de_thi: {sorted(de_thi_migrations)}")
    
    # Check applied migrations from database
    with connection.cursor() as cursor:
        cursor.execute("SELECT app, name FROM django_migrations WHERE app = %s ORDER BY id", ['de_thi'])
        db_migrations = [row[1] for row in cursor.fetchall()]
    
    print(f"Applied migrations in database: {db_migrations}")
    
    # Find missing migrations
    missing_from_db = set(de_thi_migrations) - set(db_migrations)
    missing_from_disk = set(db_migrations) - set(de_thi_migrations)
    
    if missing_from_db:
        print(f"Migrations in disk but not in DB: {missing_from_db}")
    if missing_from_disk:
        print(f"Migrations in DB but not in disk: {missing_from_disk}")
    
    # Check for dependency issues
    print("\n=== Checking Dependencies ===")
    for migration_name in sorted(de_thi_migrations):
        migration_key = ('de_thi', migration_name)
        if migration_key in loader.disk_migrations:
            migration = loader.disk_migrations[migration_key]
            dependencies = [dep for dep in migration.dependencies if dep[0] == 'de_thi']
            print(f"{migration_name}: dependencies = {dependencies}")
            
            # Check if dependencies exist
            for dep_app, dep_name in dependencies:
                if dep_app == 'de_thi':
                    dep_key = (dep_app, dep_name)
                    if dep_key not in loader.disk_migrations:
                        print(f"ERROR: {migration_name} depends on {dep_app}.{dep_name} which doesn't exist!")

if __name__ == '__main__':
    check_migration_state()