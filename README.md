cline
=====

PAT-M Anti-Corruption Hotline

* VoiceXML IVR to record messages.
* 2N Office Route POP3/SMTP SMS Gateway to record messages.
* Web Interface to display reports


# sox 0.short-intro.pcm.wav -r 8k -b 8 -e u-law -c 1 0.short-intro.wav
# ./manage.py runserver 0.0.0.0:8000
# DJANGO_SETTINGS_MODULE="cline.settings" celery -A ivr.tasks worker --loglevel=info
# ./manage.py sms_poll_service