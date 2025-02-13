from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.utils import OperationalError, ProgrammingError

def create_periodic_tasks(sender, **kwargs):
    """Ensure periodic tasks are created only after migrations are applied."""
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    import json

    try:
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=5, period=IntervalSchedule.MINUTES
        )
        if not PeriodicTask.objects.filter(name="Fetch Crypto Prices").exists():
            PeriodicTask.objects.create(
                interval=schedule,
                name="Fetch Crypto Prices",
                task="crypto_app.tasks.fetch_crypto_prices",
                args=json.dumps([]),
            )
            print("Celery periodic task registered successfully!")

    except (OperationalError, ProgrammingError):
        print("Skipping Celery task creation (DB not ready yet).")

class CryptoAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crypto_app"

    def ready(self):
        import crypto_app.signals 
        post_migrate.connect(create_periodic_tasks, sender=self) # Running after the db setup for mitigating abrupt changes
