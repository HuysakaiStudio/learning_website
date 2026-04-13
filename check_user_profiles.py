from django.contrib.auth.models import User
from apps.nguoi_dung.models import UserGamification, UserProfile
from apps.de_thi.models import UserAnalytics

def check_user_profiles():
    # Check if user analytics exist for a sample user
    try:
        user = User.objects.first()
        if user:
            print(f'Testing with user: {user}')
            
            # Check if UserAnalytics exists
            try:
                analytics = UserAnalytics.objects.get(nguoi_dung=user)
                print(f'✓ UserAnalytics exists: {analytics}')
            except UserAnalytics.DoesNotExist:
                print('✗ UserAnalytics does not exist for this user')
            
            # Check if UserGamification exists
            try:
                gamification = UserGamification.objects.get(user=user)
                print(f'✓ UserGamification exists: {gamification}')
            except UserGamification.DoesNotExist:
                print('✗ UserGamification does not exist for this user')
                
            # Check if UserProfile exists
            try:
                profile = UserProfile.objects.get(user=user)
                print(f'✓ UserProfile exists: {profile}')
            except UserProfile.DoesNotExist:
                print('✗ UserProfile does not exist for this user')
        else:
            print('No users found in the database')
            
    except Exception as e:
        print(f'Error testing user data: {e}')

if __name__ == "__main__":
    check_user_profiles()