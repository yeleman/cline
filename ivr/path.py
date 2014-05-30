#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

AUDIO_FOLDER = os.path.join(settings.BASE_DIR, 'audio', settings.IVR_VOICE)
REPORT_FOLDER = os.path.join(settings.BASE_DIR, 'reports')
