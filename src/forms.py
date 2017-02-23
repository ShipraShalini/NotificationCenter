import re

from django import forms
from django.core.exceptions import ValidationError

from src import notification_utils
from src.constants import ACTIONS

regex = re.compile('^select', re.I)


class NotificationForm(forms.Form):
    """ Form for storing notificaiton details """

    query = forms.CharField(max_length=300)
    title = forms.CharField(min_length=20, max_length=150, label='Header')
    body = forms.CharField(min_length=20, max_length=300, widget=forms.Textarea, label='Content')
    image_url = forms.URLField(widget=forms.URLInput)
    notification_time = forms.DateTimeField(widget=forms.DateTimeInput)

    def clean_notification_time(self):
        """
        validates date
        :return: date
        """
        date = self.cleaned_data['notification_time']
        notification_utils.is_valid_date(date)
        return date

    def clean_query(self):
        """
        validates date
        :return: date
        """
        query = self.cleaned_data['query']
        if not regex.match(query):
            ValidationError("Only SELECT query is valid")
        return query

    def schedule_notification(self):
        """
        schedules notifications
        :return: job_id
        """
        time = self.cleaned_data.pop('notification_time')
        query = self.cleaned_data.pop('query')
        return notification_utils.add_notification(payload=self.cleaned_data, query=query, time=time)


class ModifyNotificationForm(forms.Form):
    """ Form for modifying notifications."""

    action = forms.ChoiceField(choices=ACTIONS, widget=forms.RadioSelect)
    job_id = forms.CharField()
    query = forms.CharField(max_length=300, required=False, label='Query')
    title = forms.CharField(min_length=20, max_length=150, required=False, label='Header')
    body = forms.CharField(min_length=20, max_length=300, widget=forms.Textarea, required=False, label='Content')
    image_url = forms.URLField(required=False, widget=forms.URLInput)
    notification_time = forms.DateTimeField(required=False, widget=forms.DateTimeInput)

    def clean_notification_time(self):
        """
        validates date
        :return: date
        """
        date = self.cleaned_data['notification_time']
        if date:
            notification_utils.is_valid_date(date)
        return date

    def clean_query(self):
        """
        validates date
        :return: date
        """
        query = self.cleaned_data['query']
        if not regex.match(query):
            ValidationError("Only SELECT query is valid")
        return query

    def modify(self):
        """
        modifies notifications
        :return: job_id, action
        """
        action = self.cleaned_data.pop('action')
        job_id = self.cleaned_data.pop('job_id')
        function = getattr(notification_utils, (action + '_notification'))
        job_id, action = function(job_id=job_id, **self.cleaned_data)
        return job_id, action
