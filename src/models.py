# from django.contrib.auth import models
# from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import connection
from django.db.models import fields, Model, Manager
from django.utils.translation import ugettext_lazy as _


class UserManager(Manager):
    def get_notification_query(self, query):
        new_query = list(query.partition('from'))
        new_query[0] = 'SELECT fcm_id '
        query = ''.join(new_query)

        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
        return row


class User(Model):
    username_validator = UnicodeUsernameValidator()
    username = fields.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = fields.CharField(_('first name'), max_length=30, blank=True)
    last_name = fields.CharField(_('last name'), max_length=30, blank=True)
    email = fields.EmailField(_('email address'), blank=True)
    password = fields.CharField(_('password'), max_length=255, blank=True)
    fcm_id = fields.CharField(_('fcm id'), max_length=255, blank=True)

    objects = UserManager()
