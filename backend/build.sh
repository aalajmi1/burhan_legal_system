#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")
full_name = os.environ.get("ADMIN_FULL_NAME", "Admin")

if email and password:
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "full_name": full_name,
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
            "role": "Admin",
        },
    )

    user.full_name = full_name
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.role = "Admin"
    user.set_password(password)
    user.save()

    print(f"Superuser ready: {email}")
else:
    print("ADMIN_EMAIL or ADMIN_PASSWORD is missing. Skipping superuser creation.")
EOF
