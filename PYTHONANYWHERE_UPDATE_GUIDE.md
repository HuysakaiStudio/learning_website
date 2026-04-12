# Updating Your PythonAnywhere Application with Latest Changes

This guide will walk you through updating your PythonAnywhere hosted application with the latest changes from your GitHub repository.

## Prerequisites

- Your application is already deployed and running on PythonAnywhere
- You have access to your PythonAnywhere account
- Your code is pushed to the GitHub repository

## Steps to Update Your PythonAnywhere Deployment

### 1. Access Your PythonAnywhere Account
- Log in to your PythonAnywhere account at https://www.pythonanywhere.com/
- Go to the "Consoles" tab and launch a "Bash" console (or SSH to your account)

### 2. Navigate to Your Project Directory
```bash
cd ~/your-pythonanywhere-username.pythonanywhere.com  # Replace with your actual path
# Or navigate to wherever you originally cloned your project
```

### 3. Pull the Latest Changes from GitHub
```bash
git pull origin main
# Or whatever branch you're deploying from
```

### 4. Update Dependencies
```bash
# Activate your virtual environment
workon your-virtualenv-name  # Replace with your actual virtual environment name
# If you don't remember the name, list them with: ls ~/.virtualenvs/

# Install any new dependencies
pip install -r requirements.txt
```

### 5. Run Database Migrations (if any)
```bash
python manage.py migrate
```

### 6. Collect Static Files (if any changes)
```bash
python manage.py collectstatic --noinput
```

### 7. Restart Your Web Application
- Go to the "Web" tab in your PythonAnywhere dashboard
- Click the "Reload" button for your web application
- Alternatively, you can restart from the console:
```bash
sudo service apache2 reload
# Or if using a custom WSGI file, restart your application through the dashboard
```

## Verification Steps

### 1. Check Application Status
- Visit your application URL to verify it's running correctly
- Check for any error messages

### 2. Run the Deployment Check Script
```bash
bash check_deploy.sh
```
This script will verify your deployment setup and highlight any potential issues.

### 3. Check Logs (if there are issues)
- Check error logs in the "Web" tab under "Log files"
- Or via console: `tail -f ~/.virtualenvs/your-env-name/error.log`

## Common Issues and Solutions

### 1. Virtual Environment Issues
- Make sure your virtual environment is activated before running pip install
- Check that all dependencies in requirements.txt are compatible with PythonAnywhere's environment

### 2. Database Migration Issues
- Run migrations from the Bash console with virtual environment activated
- Check that your database settings are correct for production

### 3. Static Files Issues
- Ensure the static files directory is properly configured
- Make sure collectstatic has been run after any CSS/JS changes

### 4. Permissions Issues
- Make sure your WSGI file has the correct permissions
- Verify file ownership if you encounter permission errors

## Additional Tips

### Setting Up Automatic Deployments (Optional)
1. Go to the "Web" tab
2. Find your application and click "Advanced"
3. Set up a webhook in your GitHub repository to automatically deploy when you push changes
4. Configure the webhook to trigger on pushes to your main branch

### Backup Before Major Updates
- Consider backing up your database before major updates:
```bash
python manage.py dumpdata > backup.json
```

### Environment Variables
- Ensure all required environment variables are set in your PythonAnywhere account
- Check that sensitive data is not exposed in your repository

## Troubleshooting

If your application doesn't work after the update:

1. Check the error logs in the "Web" tab
2. Verify that the virtual environment is activated
3. Confirm that all migrations have been applied
4. Ensure static files have been collected
5. Verify that your requirements.txt includes all necessary packages
6. Check that your settings are appropriate for production (DEBUG=False, ALLOWED_HOSTS, etc.)

## Rollback Option

If the new version has critical issues, you can temporarily rollback by:

1. Going to your project directory
2. Checking out the previous stable commit: `git checkout <previous-commit-hash>`
3. Running the deployment steps again
4. Reloading your web application