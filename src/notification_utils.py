import json
import logging

import pytz
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

from src import scheduler
from src.constants import *

logger = logging.getLogger('notification')


def add_notification(payload, user_ids, time):
    """
    adds notification to the scheduler
    :param payload: content of notification
    :param user_ids: user_ids of the users to whom the notification is to be sent
    :param time: execution time of the notification
    :return: job_id
    """
    job_return = scheduler.add_job(send_notification, 'date', run_date=time, misfire_grace_time=300,
                                   kwargs={'user_ids': user_ids, 'payload': payload})
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


def modify_notification(job_id, user_ids, header, content, image_url, **kwargs):
    """
    modifies the content of scheduled notification
    :param job_id: job_id of the scheduled notification
    :param user_ids: user_ids provided by user
    :param header: header provided by user
    :param content: content provided by user
    :param image_url: image_url provided by user
    :param kwargs: extra info provided by user
    :return: job id and action
    """
    payload = {
        "header": header,
        "content": content,
        "image_url": image_url,
    }
    job_return = scheduler.modify_job(job_id=job_id, jobstore='default',
                                      kwargs={'user_ids': user_ids, 'payload': payload})
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


def send_notification(user_ids, payload):
    """
    dummy function to send notification to users
    :param user_ids: user_ids to be queried from db
    :param payload: data for sendng notification
    :return: None
    """
    data = {
        "user_ids": user_ids,
        "payload": payload
    }
    logger.info(json.dumps(data))


def is_valid_date(date):
    """
    checks if the time provided is at least a minute more than the current time
    If not, raises ValidationError
    :return: None
    """
    one_minute_from_now = pytz.utc.localize(datetime.utcnow() + timedelta(minutes=1))
    if date < one_minute_from_now:
        raise ValidationError("The notification_time must be 1 min more than current time")