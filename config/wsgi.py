# config/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Auto-create superuser if not present
try:
    from django.contrib.auth import get_user_model
    from django.core.management import call_command

    call_command('migrate', interactive=False)

    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpassword123"
        )
        print("✅ Superuser created: admin / adminpassword123")
except Exception as e:
    print("⚠️ Admin auto-creation failed:", e)
