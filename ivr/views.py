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
from django.http import HttpResponse, Http404
from django.views.static import serve as static_serve
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

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
    return do_serve_file_no_auth(request, fname=fname, folder=AUDIO_FOLDER)


@login_required
def mp3_download(request, reportID):
    report = Report.get_or_none(reportID)
    if report is None:
        raise Http404("No report with ID {}".format(reportID))
    return do_serve_file_no_auth(request,
                                 fname=report.audio_basename(),
                                 folder=REPORT_FOLDER,
                                 as_attachment=bool(request.GET.get('dl')))


def serve_cached_file(request, fname=None, public=False):
    if not fname.startswith('public_'):
        return login_required(do_serve_file_no_auth)(request, fname)
    return do_serve_file_no_auth(request, fname)


def do_serve_file_no_auth(request,
                          fname=None,
                          folder=REPORT_FOLDER,
                          as_attachment=False):
    if settings.SERVE_AUDIO_FILES:
        return static_serve(request, fname, folder, True)
    response = HttpResponse()
    del response['content-type']
    target = 'protected_dl' if as_attachment else 'protected'
    response['X-Accel-Redirect'] = "/{target}/{fname}".format(target=target,
                                                              fname=fname)
    return response


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


@login_required
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
