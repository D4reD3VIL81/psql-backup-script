from celery import Celery
from celery.schedules import crontab
from .main import backup_postgresql_data

app = Celery("backup_task", broker="redis://redis:6379/0")

# Configure the Celery beat schedule
app.conf.beat_schedule = {
    "weekly_backup": {
        "task": "tasks.weekly_backup",
        "schedule": crontab(minute=0, hour=0, day_of_week="sunday"),  # Every Sunday at midnight
    },
}
app.conf.timezone = "UTC"

@app.task
def weekly_backup():
    """
    Task to back up PostgreSQL data.
    """
    backup_postgresql_data()
