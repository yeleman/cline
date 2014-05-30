#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os
import tempfile
import logging

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.static import serve as static_serve
from django.views.decorators.csrf import csrf_exempt

from ivr.path import AUDIO_FOLDER, REPORT_FOLDER
from ivr.utils import number_from_callerID
from ivr.models import Report

logger = logging.getLogger(__name__)


def store_uploaded_file(f, report):
    fpath = report.audio_basename(raw=True)
    fwav = open(fpath, 'wb+')
    for chunk in f.chunks():
        fwav.write(chunk)
    fwav.close()

def audio_download(request, fname):
    return static_serve(request, fname, AUDIO_FOLDER, True)


def mp3_download(request, reportID):
    report = Report.get_or_none(reportID)
    if report is None:
        raise Http404("No report with ID {}".format(reportID))
    return static_serve(request, report.audio_basename(), REPORT_FOLDER, True)


@csrf_exempt
def ivr_valid_agreement(request):
    context = {}
    print("valid_agreement")
    print(request.GET)
    report = Report.get_or_none(request.GET.get('reportID'))
    if report is not None:
        report.agreement = True
        report.save()
    return render(request,
                  'after_agreement.xml',
                  context,
                  content_type='application/xml')


@csrf_exempt
def ivr_upload(request):
    context = {}
    print("upload")
    print(request.GET)
    identity = number_from_callerID(request.GET.get('callerID'))
    print("identity", identity)
    report = Report.objects.create(identity=identity,
                                   report_type=Report.TYPE_AUDIO)
    print("report", report)
    try:
        report.process_audio(request.FILES.get('recorded_report'))
        context.update({'reportID': report.id, 'report': report})
    except Exception as e:
        context.update({'reportID': None, 'report': None})
        print(e)

    return render(request,
                  'after_upload.xml',
                  context,
                  content_type='application/xml')


def home(request):

    context = {}

    context.update({
        'reports': Report.objects.all().order_by('-received_on')})
    return render(request, 'home.html', context)

def ivr_home(request):
    context = {}
    voicexml_context = {
        'parentSessionID': request.GET.get('session.parentsessionid'),
        'accountID': request.GET.get('session.accountid'),
        'calledID': request.GET.get('session.calledid'),
        'callerID': request.GET.get('session.callerid'),
        'sessionID': request.GET.get('session.sessionid'),
    }

    querystr = "&".join(["{}={}".format(k,v) for k,v in voicexml_context.items()])

    context.update(voicexml_context)
    context.update({'querystr': querystr})

    from pprint import pprint as pp ; pp(context)

    return render(request,
                  'ivr.xml',
                  context,
                  content_type='application/xml')
