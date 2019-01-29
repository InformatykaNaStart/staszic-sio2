from django.conf.urls import patterns, include, url
import views

contest_patterns = [url(r'^example-tests/(?P<pi_short>[a-z0-9-]+)/$', views.example_tests_view, name='example-tests'),
    url(r'p/(?P<problem_instance_id>[a-z0-9_-]+)/reload_tests_limits_for_probleminstance', views.reload_limits_from_config_view, name='reload_tests_limits_for_probleminstance')]