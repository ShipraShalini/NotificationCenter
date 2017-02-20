from unittest import TestCase

from datetime import datetime, timedelta
from pytz import utc

from src.forms import NotificationForm


class TestScheduleNotification(TestCase):
    def test_notification_form(self):
        form_data = {
            "query": 'user_ids',
            "header": "This is header field data",
            "content": "This is the content field data",
            "notification_time": utc.localize(datetime.utcnow() + timedelta(minutes=2)),
            "image_url": "https://image.flaticon.com/icons/png/128/118/118781.png"
        }
        form = NotificationForm(data=form_data)
        self.assertTrue(form.is_valid())

    # def

class TestModifyNotification(TestCase):
    def test_reschedule_form(self):
        form_data = {
            "job_id"
            "query": 'user_ids',
            "header": "This is header field data",
            "content": "This is the content field data",
            "notification_time": utc.localize(datetime.utcnow() + timedelta(minutes=2)),
            "image_url": "https://image.flaticon.com/icons/png/128/118/118781.png"
        }
        form = NotificationForm(data=form_data)
        self.assertTrue(form.is_valid())