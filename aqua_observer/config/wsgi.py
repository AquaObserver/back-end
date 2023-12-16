import os

from django.core.wsgi import get_wsgi_application
from aqua_observer.broker import client
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aqua_observer.config.settings')

client.loop_start()
application = get_wsgi_application()
