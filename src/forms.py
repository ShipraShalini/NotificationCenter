from datetime import datetime, timedelta

from django import forms

from src import notification_utils
from src.constants import ACTIONS




class NotificationForm(forms.Form):
    """ Form for storing notificaiton details """

    query = forms.CharField(max_length=300)
    header = forms.CharField(min_length=20, max_length=150)
    content = forms.CharField(min_length=20, max_length=300, widget=forms.Textarea)
    image_url = forms.URLField(widget=forms.URLInput)
    notification_time = forms.DateTimeField(widget=forms.DateTimeInput, initial=datetime.utcnow())

    def clean_notification_time(self):
        date = self.cleaned_data['notification_time']
        notification_utils.is_valid_date(date)
        return date

    def schedule_notification(self):
        time = self.cleaned_data.pop('notification_time')
        user_ids = self.cleaned_data.pop('query')
        return notification_utils.add_notification(payload=self.cleaned_data, user_ids=user_ids, time=time)


class ModifyNotificationForm(forms.Form):
    """ Form for modifying notifications."""

    action = forms.ChoiceField(choices=ACTIONS, widget=forms.RadioSelect)
    job_id = forms.CharField()
    query = forms.CharField(max_length=300, required=False)
    header = forms.CharField(min_length=20, max_length=150, required=False)
    content = forms.CharField(min_length=20, max_length=300, widget=forms.Textarea, required=False)
    image_url = forms.URLField(required=False, widget=forms.URLInput)
    notification_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput)

    def clean_notification_time(self):
        date = self.cleaned_data['notification_time']
        if date:
            notification_utils.is_valid_date(date)
        return date

    def modify(self):
        action = self.cleaned_data.pop('action')
        job_id = self.cleaned_data.pop('job_id')
        function = getattr(notification_utils, (action + '_notification'))
        job_id, action = function(job_id=job_id, **self.cleaned_data)
        return job_id, action
