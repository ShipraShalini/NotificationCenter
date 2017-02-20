#
# Not complete, not tested.
# use django-nose
#


from unittest import TestCase

from datetime import datetime, timedelta
from pytz import utc

from src.forms import NotificationForm
from src.notification_utils import add_notification


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



class TestModifyNotification(TestCase):

    def add_notification_for_test(self):
        payload = {
            "header": "Test:This is header field data",
            "content": "This is the content field data",
            "notification_time": utc.localize(datetime.utcnow() + timedelta(minutes=2)),
            "image_url": "https://image.flaticon.com/icons/png/128/118/118781.png"
        }
        return add_notification(payload=payload, user_ids='user_ids', time=utc.localize(datetime.utcnow() + timedelta(minutes=2)))

    def test_reschedule_form_with_all_fields(self):
        # job_id = self.add_notification_for_test()
        form_data = {
            "job_id": "job_id",
            "action": "reschedule",
            "query": 'user_ids',
            "header": "This is header field data",
            "content": "This is the content field data",
            "notification_time": utc.localize(datetime.utcnow() + timedelta(minutes=2)),
            "image_url": "https://image.flaticon.com/icons/png/128/118/118781.png"
        }
        form = NotificationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_modify_form_with_all_fields(self):
        # job_id = self.add_notification_for_test()
        form_data = {
            "job_id": "job_id",
            "action": "modify",
            "query": 'user_ids',
            "header": "This is header field data",
            "content": "This is the content field data",
            "notification_time": utc.localize(datetime.utcnow() + timedelta(minutes=2)),
            "image_url": "https://image.flaticon.com/icons/png/128/118/118781.png"
        }
        form = NotificationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_delete_form_with_all_fields(self):
        # job_id = self.add_notification_for_test()
        form_data = {
            "job_id": "job_id",
            "action": "remove",
            "query": 'user_ids',
            "header": "This is header field data",
            "content": "This is the content field data",
            "notification_time": utc.localize(datetime.utcnow() + timedelta(minutes=2)),
            "image_url": "https://image.flaticon.com/icons/png/128/118/118781.png"
        }
        form = NotificationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reschedule_form(self):
        # job_id = self.add_notification_for_test()
        form_data = {
            "job_id": "job_id",
            "action": "reschedule",
            "notification_time": utc.localize(datetime.utcnow() + timedelta(minutes=2)),
        }
        form = NotificationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_modify_form(self):
        # job_id = self.add_notification_for_test()
        form_data = {
            "job_id": "job_id",
            "action": "modify",
            "query": 'user_ids',
            "header": "This is header field data",
            "content": "This is the content field data",
            "image_url": "https://image.flaticon.com/icons/png/128/118/118781.png"
        }
        form = NotificationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_delete_form(self):
        # job_id = self.add_notification_for_test()
        form_data = {
            "job_id": "job_id",
            "action": "remove",
        }
        form = NotificationForm(data=form_data)
        self.assertTrue(form.is_valid())
