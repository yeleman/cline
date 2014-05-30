#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import time

from django.core.management.base import BaseCommand
from django.conf import settings

from ivr.email import get_emails

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        while(True):
            get_emails()
            time.sleep(settings.VOICE_POP3_POLL_INTERVAL)
