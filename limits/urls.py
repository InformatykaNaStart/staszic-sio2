from django.conf.urls import patterns, include, url
import views

contest_patterns = [url(r'limits/(\d+)', views.limits_view, name='limits')]

