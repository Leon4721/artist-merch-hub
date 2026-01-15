import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Run DB migrations
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    print("⚠️ Auto migration failed:", e)

# Auto create superuser for Render free tier
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "adminpassword123")
        print("✅ Superuser created: admin / adminpassword123")
except Exception as e:
    print("⚠️ Superuser creation failed:", e)

application = get_wsgi_application()
