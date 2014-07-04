#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import poplib
import email

from dateutil.parser import parse as dt_parse
from django.conf import settings
from django.utils import timezone

from ivr.models import SMSMessage, Report
from ivr.utils import send_sms, notify_new_report

logger = logging.getLogger(__name__)


def get_emails():
    # connect
    logger.info("[EMAIL] Connecting to server {}".format(settings.VOICE_POP3_SERVER))
    psrv = poplib.POP3(settings.VOICE_POP3_SERVER, settings.VOICE_POP3_PORT)
    psrv.user(settings.VOICE_POP3_USER)
    psrv.pass_(settings.VOICE_POP3_PASSWD)

    # get inbox count
    numMessages = len(psrv.list()[1])
    logger.info("[EMAIL] {} messages to process from gateway.".format(numMessages))

    # loop on message source
    for i in range(1, numMessages + 1):
        message = "\n".join([s.decode('utf-8') for s in psrv.retr(i)[1]])
        # for message in psrv.retr(i)[1]:
        try:
            # sets the read flag (which should delete as per gateway config)
            handle_incoming_email(message)
        except:
            logger.error("Unable to process message #{}: {}".format(i, message))
        finally:
            psrv.dele(i)

    # commit changes and quit
    logger.info("[EMAIL] Committing changes and quit.")
    psrv.quit()

def handle_incoming_email(message):
    msg = email.message_from_string(message.encode('utf-8'))
    text = msg.get_payload().strip().decode('utf-8')
    received_on = dt_parse(msg.get('Date').strip()).replace(tzinfo=timezone.utc)
    identity = msg.get('From').strip().split('@', 1)[0]
    sms = SMSMessage(identity=identity,
                     text=text,
                     received_on=received_on)
    logger.info("Incoming SMS {}".format(sms))
    try:
        return handle_incoming_sms(sms)
    except Exception as exp:
        logger.error("Exception in handling {}: {}".format(sms, exp))
        return None

def handle_incoming_sms(sms):
    # print("From: {}\nDate: {}\nContent: {}".format(sms.identity, sms.received_on, sms.text))

    # check if SMS is valid (exclude operator and spam)
    if sms.identity is not "SIP" and len(sms.identity) < 8:
        logger.info("Excluded invalid SMS from {}/{}:{}"
                    .format(sms.identity, sms.received_on, sms.text))
        return None

    # set agreement is it's an answer to agreement request
    if sms.is_agreement:
        report = Report.last_from(sms.identity, report_types=[Report.TYPE_TEXT])
        if report is not None and not report.agreement:
            logger.info("Agreement received from {}".format(sms.identity))
            report.ack_agreement()
            return report
        logger.info("Useless agreement received from {}".format(sms.identity))
        return None

    # new incoming report
    report, created = Report.objects.get_or_create(
        identity=sms.identity,
        received_on=sms.received_on,
        text=sms.text,
        report_type=Report.TYPE_TEXT)
    logger.info("{}: {}".format("created" if created else "duplicate", report))

    if created:
        send_sms(sms.identity, settings.VOICE_AGREEMENT_MESSAGE)
        notify_new_report.apply_async([report])

    return report
