#!/usr/bin/env python
"""Script to check if the hinh_anh field exists in the CauHoi model"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def check_image_field():
    """Check if the hinh_anh field exists in the CauHoi model"""
    django.setup()
    
    from apps.de_thi.models import CauHoi
    
    # Get the model fields
    fields = [f.name for f in CauHoi._meta.get_fields()]
    
    print("Fields in CauHoi model:")
    for field in fields:
        print(f"- {field}")
    
    if 'hinh_anh' in fields:
        print("\n✓ SUCCESS: hinh_anh field exists in the CauHoi model!")
        
        # Get field info
        field = CauHoi._meta.get_field('hinh_anh')
        print(f"Field type: {type(field).__name__}")
        print(f"Upload to: {getattr(field, 'upload_to', 'N/A')}")
        print(f"Null allowed: {field.null}")
        print(f"Blank allowed: {field.blank}")
    else:
        print("\n✗ ERROR: hinh_anh field NOT found in the CauHoi model!")

if __name__ == "__main__":
    check_image_field()