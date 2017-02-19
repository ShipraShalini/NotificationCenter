from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from django import forms
from django.conf import settings

from src.logic import send_notification

scheduler = BackgroundScheduler(settings.APSCHEDULER_SETTINGS)

scheduler.start()



class NotificationForm(forms.Form):
    """ Form for storing notificaiton details """

    query = forms.CharField(max_length=300)
    header = forms.CharField(min_length=20, max_length=150)
    content = forms.CharField(min_length=20, max_length=300, widget=forms.Textarea)
    image_url = forms.URLField(widget=forms.URLInput)
    notification_time = forms.DateTimeField(widget=forms.DateTimeInput)

    def schedule_notification(self):
        time = self.cleaned_data.pop('notification_time')
        user_ids = self.cleaned_data.pop('query')
        job_return = scheduler.add_job(send_notification, 'date', run_date=time,
                                       kwargs={'user_ids': user_ids, 'payload': self.cleaned_data})
        return job_return.id


class ModifyNotificationForm(forms.Form):
    """ Form for storing notificaiton details """

    ACTIONS = (
        ('reschedule', 'Reschedule',),
        ('modify', 'Modify'),
        ('remove', 'Remove'),
    )
    action = forms.ChoiceField(choices=ACTIONS, widget=forms.RadioSelect)
    job_id = forms.CharField()
    query = forms.CharField(max_length=300, required=False)
    header = forms.CharField(min_length=20, max_length=150, required=False)
    content = forms.CharField(min_length=20, max_length=300, widget=forms.Textarea, required=False)
    image_url = forms.URLField(required=False, widget=forms.URLInput)
    notification_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput)

    @staticmethod
    def reschedule_notification(job_id, notification_time, **kwargs):
        job_return = scheduler.reschedule_job(job_id=job_id, jobstore='default', trigger='date',
                                              run_date=notification_time)
        return job_return.id, "rescheduled"

    @staticmethod
    def modify_notification(job_id, query, header, content, image_url, **kwargs):
        payload = {
            "header": header,
            "content": content,
            "image_url": image_url,
        }
        job_return = scheduler.modify_job(job_id=job_id, jobstore='default',
                                          kwargs={'user_ids': query, 'payload': payload})
        return job_return.id, "modified"

    @staticmethod
    def remove_notification(job_id, **kwargs):
        scheduler.remove_job(job_id=job_id, jobstore='default')
        return job_id, "removed"

    def modify(self):
        action = self.cleaned_data.pop('action')
        job_id = self.cleaned_data.pop('job_id')
        function = getattr(self, (action + '_notification'))
        job_id, action = function(job_id=job_id, **self.cleaned_data)
        return job_id, action
