#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from ivr.email import get_emails

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_emails()
