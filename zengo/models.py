# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from konst import Constant, Constants
from konst.models.fields import ConstantChoiceCharField


AUTH_USER_MODEL = get_user_model()


class ZendeskUser(models.Model):
    """
    Link between a user in Zendesk and the local system.

    Depending on how users access Zendesk services, it may sometime
    not be possible to link all Zendesk users to local users, so `user`
    can be null.
    """

    class Meta:
        app_label = 'zengo'

    id = models.BigAutoField(primary_key=True)
    zendesk_id = models.BigIntegerField(unique=True)
    name = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True)
    created = models.DateTimeField()


class Ticket(models.Model):

    class Meta:
        app_label = 'zengo'

    id = models.BigAutoField(primary_key=True)
    zendesk_id = models.BigIntegerField(unique=True)
    zendesk_user = models.ForeignKey(ZendeskUser)
    subject = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    states = Constants(
        Constant(new='new'),
        Constant(open='open'),
        Constant(pending='pending'),
        Constant(hold='hold'),
        Constant(solved='solved'),
        Constant(closed='closed')
    )
    status = ConstantChoiceCharField(constants=states, max_length=8)
    created = models.DateTimeField()
    updated = models.DateTimeField(null=True, blank=True)


class Comment(models.Model):

    class Meta:
        app_label = 'zengo'

    id = models.BigAutoField(primary_key=True)
    zendesk_id = models.BigIntegerField(unique=True)
    ticket = models.ForeignKey(Ticket)
    author = models.ForeignKey(ZendeskUser)
    body = models.TextField(null=True, blank=True)
    public = models.BooleanField()
    created = models.DateTimeField()
    # our custom fields
    notified = models.BooleanField(default=False)


class Event(models.Model):

    class Meta:
        app_label = 'zengo'

    raw_data = models.TextField()
    json = models.JSONField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)
    # if processing failed there was an error, it will appear here
    error = models.TextField(null=True, blank=True)
    # these should be populated if it was processed OK
    ticket = models.ForeignKey(Ticket, null=True, blank=True)
    actor = models.ForeignKey(ZendeskUser, null=True, blank=True)