import os
from celery import Celery
from dotenv import load_dotenv
from django.apps import apps

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_project.settings')

app = Celery('crypto_project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")