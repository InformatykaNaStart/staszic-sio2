from django.conf.urls import patterns, include, url
import views

contest_patterns = [url(r'^example-tests/(?P<pi_short>[a-z0-9-]+)/$', views.example_tests_view, name='example-tests')]

