#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django import template
from django.template.defaultfilters import stringfilter #  , date

from ivr.utils import phonenumber_repr

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter(name='phone')
@stringfilter
def phone_number_formatter(number):
    ''' format phone number properly for display '''
    if number == 'SIP':
        return number
    return phonenumber_repr(number)
