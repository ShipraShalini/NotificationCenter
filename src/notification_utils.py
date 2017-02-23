import logging
from datetime import datetime, timedelta

import pytz
from django.core.exceptions import ValidationError

from src import scheduler
from src.constants import *
from src.gcmnotifications import FcmNotifications
from src.models import User

logger = logging.getLogger('notification')


def add_notification(payload, query, time):
    """
    adds notification to the scheduler
    :param payload: body of notification
    :param query: SQL query to get the users to whom the notification is to be sent
    :param time: execution time of the notification
    :return: job_id
    """
    fcm_list = User.objects.get_notification_query(query)
    job_return = scheduler.add_job(send_notification, 'date', run_date=time, misfire_grace_time=300,
                                   kwargs={'fcm_list': fcm_list, 'payload': payload})
    return job_return.id


def reschedule_notification(job_id, notification_time, **kwargs):
    """
    modifies the execution time of scheduled notification
    :param job_id: job_id of the scheduled notification
    :param notification_time: new notification_time
    :param kwargs: extra info provided by user
    :return: job id and action
    """
    job_return = scheduler.reschedule_job(job_id=job_id, jobstore='default', trigger='date',
                                          run_date=notification_time)
    return job_return.id, RESCHEDULED


def modify_notification(job_id, payload, query, **kwargs):
    """
    modifies the body of scheduled notification
    :param job_id: job_id of the scheduled notification
    :param query: SQL query to get the users to whom the notification is to be sent
    :param title: title provided by user
    :param body: body provided by user
    :param image_url: image_url provided by user
    :param kwargs: extra info provided by user
    :return: job id and action
    """
    fcm_list = User.objects.get_notification_query(query)
    job_return = scheduler.modify_job(job_id=job_id, jobstore='default',
                                      kwargs={'fcm_list': fcm_list, 'payload': payload})
    return job_return.id, MODIFIED


def remove_notification(job_id, **kwargs):
    """
    removes the scheduled notification
    :param job_id: job_id of the scheduled notification
    :param kwargs: extra fields entered by the user
    :return: job id and action
    """
    scheduler.remove_job(job_id=job_id, jobstore='default')
    return job_id, REMOVED


def send_notification(fcm_list, payload):
    """
    function to send notification to users
    :param query: fcm_ids of the users to whom the notification is to be sent
    :param payload: data for sendng notification
    :return: None
    """
    FcmNotifications().send(fcm_list=fcm_list, data=payload)


def is_valid_date(date):
    """
    checks if the time provided is at least a minute more than the current time
    If not, raises ValidationError
    :return: None
    """
    one_minute_from_now = pytz.utc.localize(datetime.utcnow() + timedelta(minutes=1))
    if date < one_minute_from_now:
        raise ValidationError("The notification_time must be 1 min more than current time")
