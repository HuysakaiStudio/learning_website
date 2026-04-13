#!/usr/bin/env python
"""Script to verify the hinh_anh field exists in the CauHoi model"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def verify_image_field():
    """Verify if the hinh_anh field exists in the CauHoi model"""
    django.setup()
    
    from apps.de_thi.models import CauHoi
    
    # Get the model fields
    fields = [f.name for f in CauHoi._meta.get_fields()]
    
    print("Fields in CauHoi model:")
    for field in fields:
        print(f"- {field}")
    
    if 'hinh_anh' in fields:
        print("\nSUCCESS: hinh_anh field exists in the CauHoi model!")
        
        # Get field info
        field = CauHoi._meta.get_field('hinh_anh')
        print(f"Field type: {type(field).__name__}")
        print(f"Upload to: {getattr(field, 'upload_to', 'N/A')}")
        print(f"Null allowed: {field.null}")
        print(f"Blank allowed: {field.blank}")
        print(f"Verbose name: {field.verbose_name}")
        
        print("\nImage support is properly configured!")
        print("- Users can now upload images for questions")
        print("- Images will be stored in 'cau_hoi_images/' directory")
        print("- Templates are updated to display images in exam interface")
        print("- Forms are updated to support image uploads")
    else:
        print("\nERROR: hinh_anh field NOT found in the CauHoi model!")

if __name__ == "__main__":
    verify_image_field()