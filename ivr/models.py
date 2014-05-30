#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os
import logging
import subprocess
import json

from django.utils import timezone
from django.db import models

from ivr.path import REPORT_FOLDER
from ivr.utils import get_wave_duration

logger = logging.getLogger(__name__)


class Report(models.Model):

    TYPE_AUDIO = 'audio'
    TYPE_TEXT = 'text'
    TYPES = {
        TYPE_AUDIO: "Audio",
        TYPE_TEXT: "Text"
    }

    identity = models.CharField(max_length=200)
    received_on = models.DateTimeField(default=timezone.now)
    report_type = models.CharField(max_length=100, choices=TYPES.items())
    agreement = models.BooleanField(default=False)

    # audio only
    duration = models.IntegerField(null=True, blank=True)

    # text only
    text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{identity} on {time}".format(identity=self.identity,
                                             time=self.received_on)

    def to_dict(self):
        return {
            'id': self.id,
            'identity': self.identity,
            'received_on': self.received_on.isoformat(),
            'report_type': self.report_type,
            'agreement': self.agreement,
            'duration': self.duration,
            'text': self.text
        }

    def export(self):
        with open('report_{id}.json'.format(id=self.id)) as f:
            json.dump(self.to_dict(), f)

    def is_text(self):
        return self.report_type == self.TYPE_TEXT

    def audio_exists(self, raw=False):
        return os.path.exists(self.audio_path(raw))

    def audio_basename(self, raw=False):
        ext = "wav" if raw else "mp3"
        return "report_{id}.{ext}".format(id=self.id, ext=ext)

    def audio_path(self, raw=False):
        return os.path.join(REPORT_FOLDER, self.audio_basename(raw))

    def public_identity(self):
        l = len(self.identity)
        if self.agreement or l <= 3:
            return self.identity
        return "x".join(['' for _ in range(l - 2)]) + self.identity[-2:]

    def method(self):
        return self.TYPES.get(self.report_type)

    def update_duration(self):
        try:
            duration = get_wave_duration(self.audio_path(raw=True))
            self.duration = int(duration)
            self.save()
        except:
            pass

    def ack_agreement(self):
        self.agreement = True
        self.save()

    def process_audio(self, uploaded_file):
        self.store_original_file(uploaded_file)
        self.update_duration()
        self.convert_to_mp3()

    def store_original_file(self, uploaded_file):
        fwav = open(self.audio_path(raw=True), 'w')
        for chunk in uploaded_file.chunks():
            fwav.write(chunk)
        fwav.close()

    def convert_to_mp3(self):
        cmd = "lame -m mo -t {src} {dst}".format(
            src=self.audio_path(raw=True),
            dst=self.audio_path())
        subprocess.Popen(cmd.split())

    @classmethod
    def get_or_none(cls, id):
        try:
            return cls.objects.get(id=id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def last_from(cls, identity, report_types=(TYPE_TEXT, TYPE_AUDIO)):
        try:
            return cls.objects.filter(identity=identity) \
                              .filter(report_type__in=report_types) \
                              .order_by('received_on').last()
        except (cls.DoesNotExist, IndexError):
            return None


class SMSMessage(object):

    def __init__(self, identity, text, received_on=None):
        self.identity = identity.strip()
        self.text = text.strip()
        self.received_on = received_on or timezone.now()
        self.is_agreement = self._is_agreement()

    def __unicode__(self):
        return "{}: {}".format(self.identity, self.text)

    def _is_agreement(self):
        if self.text.lower().strip() in ('oui', 'o', 'yes', 'y', 'ok', 'k'):
            return True
        return False

