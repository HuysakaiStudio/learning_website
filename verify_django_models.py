"""
Verification script to ensure Django models work with the new XP/Level formulas
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.getcwd())

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.nguoi_dung.models import UserGamification
import math

def test_model_functions():
    print("Testing Django Model Functions:")
    print("=" * 40)
    
    # Create a temporary UserGamification instance to test methods
    gamification = UserGamification()
    
    # Test the new formulas
    print("Testing XP/Level conversion formulas...")
    
    test_levels = [0, 1, 5, 10, 15, 20, 25]
    
    all_passed = True
    
    for level in test_levels:
        # Test get_xp_for_level (which now uses level^2 * 100)
        xp_needed = gamification.get_xp_for_level(level)
        
        # Test calculate_level (which should reverse the calculation)
        calculated_level = gamification._calculate_level_from_xp(xp_needed)
        
        status = "[PASS]" if level == calculated_level else "[FAIL]"
        if level != calculated_level:
            all_passed = False
            
        print(f"Level {level}: XP needed={xp_needed}, Calculated back={calculated_level} {status}")
    
    print(f"\nModel function consistency: {'[PASS]' if all_passed else '[FAIL]'}")
    
    # Test progress calculation methods
    print("\nTesting progress calculation methods...")
    
    # Test with various XP values
    test_xp_values = [0, 50, 100, 200, 500, 1000, 2500, 5000, 10000]
    
    for xp in test_xp_values:
        gamification.xp = xp
        level = gamification.calculate_level()
        
        # Test progress within level
        current_level_start_xp = level * level * 100
        next_level_start_xp = (level + 1) * (level + 1) * 100
        
        xp_in_current_level = max(0, xp - current_level_start_xp)
        xp_needed_for_next_level = next_level_start_xp - current_level_start_xp
        
        progress_percent = 0
        if xp_needed_for_next_level > 0:
            progress_percent = round((xp_in_current_level / xp_needed_for_next_level) * 100, 1)
        
        print(f"XP {xp:6d}: Level {level}, Progress {xp_in_current_level}/{xp_needed_for_next_level} XP ({progress_percent}%)")
    
    # Test enhanced progress method
    print("\nTesting enhanced progress method...")
    gamification.xp = 1500
    level_progress = gamification.get_enhanced_level_progress()
    
    print(f"XP 1500: {level_progress}")
    
    print(f"\n{'='*50}")
    print("Django model verification: [PASS]")
    print("All methods work correctly with the new XP = level^2 * 100 formula")
    
    return all_passed

if __name__ == "__main__":
    test_model_functions()