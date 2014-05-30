#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

from ivr.email import get_emails

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("Synchonizing Database and MP3 files with server.")
        cmd = "rsync -av django.sqlite3 reports {url}".format(url=settings.SYNCHRO_URL)
        subprocess.call(cmd.split())
        logger.info("Synchonization complete.")

