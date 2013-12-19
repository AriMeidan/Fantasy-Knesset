from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^votes/', include('votes.urls')),
    url(r'^admin/', include(admin.site.urls)),
)