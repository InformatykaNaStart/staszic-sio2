from django.conf.urls import patterns, include, url
import views

noncontest_patterns = [url(r'^staszic/judging/(?P<jid>\d+)/$', views.judging)]
