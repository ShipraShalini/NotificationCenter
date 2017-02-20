from datetime import datetime, timedelta

import pytz
from django import forms

from src import notification_utils

utc = pytz.utc


class NotificationForm(forms.Form):
    """ Form for storing notificaiton details """

    query = forms.CharField(max_length=300)
    header = forms.CharField(min_length=20, max_length=150)
    content = forms.CharField(min_length=20, max_length=300, widget=forms.Textarea)
    image_url = forms.URLField(widget=forms.URLInput)
    notification_time = forms.DateTimeField(widget=forms.DateTimeInput, initial=datetime.utcnow())

    # def clean_notification_time(self):
    #     date = self.cleaned_data['notification_time']
    #     print "tzinfo", date.tzinfo
    #     one_minute_from_now = utc.localize(datetime.utcnow() + timedelta(minutes=1))
    #     if date < one_minute_from_now:
    #         raise forms.ValidationError("The notification_time must be 1 min more than current time")
    #     return date

    def schedule_notification(self):
        time = self.cleaned_data.pop('notification_time')
        user_ids = self.cleaned_data.pop('query')
        return notification_utils.add_notification(payload=self.cleaned_data, user_ids=user_ids, time=time)


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

    # def clean_notification_time(self):
    #     date = self.cleaned_data['notification_time']
    #     one_minute_from_now = utc.localize(datetime.utcnow() + timedelta(minutes=1))
    #     if date < one_minute_from_now:
    #         raise forms.ValidationError("The notification_time must be 1 min more than current time")
    #     return date

    def modify(self):
        action = self.cleaned_data.pop('action')
        job_id = self.cleaned_data.pop('job_id')
        function = getattr(notification_utils, (action + '_notification'))
        job_id, action = function(job_id=job_id, **self.cleaned_data)
        return job_id, action
