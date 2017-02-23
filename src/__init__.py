from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

scheduler = BackgroundScheduler(settings.APSCHEDULER_SETTINGS)

scheduler.start()
