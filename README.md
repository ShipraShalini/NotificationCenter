# Notification Creator

This project schedules notification to be sent on a specific time provided.
It can also reschedule, modify and delete scheduled notifications.
It has a grace time of 5 minutes in case the notifcation is not sent on the specified time.

The dummy function to send notification logs the data to `logs/notification.log`.

datetime should be in UTC and should be aleast one minute more than current UTC time.

For sending notification, please add your fcm key in settings file.
`FCM_KEY = 'gfk5rv6te4wrcyt75w6t6hb8trswa3'`

### Dependencies
- [APScheduler](https://apscheduler.readthedocs.io/en/latest/)
- [django-bootstrap-form](https://github.com/tzangms/django-bootstrap-form)
- [SQLAlchemy](http://www.sqlalchemy.org/)

### Usage

#### Scheduling Notifications

**http://localhost:8000/notification/**

![screenshot](https://drive.google.com/uc?id=0B00Wd-9BBxdgbTZqSzZaRm1oMkk)

#### Modifying Notifications

**http://localhost:8000/modify_notification/**

![screenshot](https://drive.google.com/uc?id=0B00Wd-9BBxdgUXpVNW1GSzJzYnc)

#### List scheduled notifications
**http://localhost:8000/get_notifications/**
