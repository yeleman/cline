#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.conf import settings
from celery import Celery

logger = logging.getLogger(__name__)

app = Celery('tasks', broker=settings.BROKER_URL)
