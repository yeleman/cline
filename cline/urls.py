from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^upload$', 'ivr.views.ivr_upload', name='upload'),
    url(r'^valid_agreement$', 'ivr.views.ivr_valid_agreement', name='valid_agreement'),
    url(r'^ivr$', 'ivr.views.ivr_home', name='intro'),
    url(r'^$', 'ivr.views.home', name='home'),

    url(r'^audio/(?P<fname>[a-zA-Z\-\.0-9]+)$', 'ivr.views.audio_download', name='audio'),
    url(r'^mp3/(?P<reportID>[0-9]+)$', 'ivr.views.mp3_download', name='mp3'),

    url(r'^admin/', include(admin.site.urls)),
)
