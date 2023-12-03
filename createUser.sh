#!/bin/bash
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')" | python3 manage.py shell