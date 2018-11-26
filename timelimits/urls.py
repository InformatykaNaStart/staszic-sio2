from django.conf.urls import patterns, include, url
import views

contest_patterns = [
        url(r'^s/(\d+)/tls/form/$', views.show_form, name='submission-set-tls-form'),
        url(r'^s/(\d+)/tls/$', views.set_timelimits, name='submission-set-tls')
    ]

