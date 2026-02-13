import os
import django

# إعداد Django للوصول إلى إعداداته
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_system.settings")
django.setup()

from django.contrib.auth.models import User

# بيانات superuser
USERNAME = "admin"
EMAIL = "admin@admin.com"
PASSWORD = "super.admin"  # ضع كلمة مرور قوية

# تحقق إذا كان المستخدم موجودًا بالفعل
if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
    print(f"Superuser '{USERNAME}' تم إنشاؤه بنجاح!")
else:
    print(f"Superuser '{USERNAME}' موجود بالفعل.")