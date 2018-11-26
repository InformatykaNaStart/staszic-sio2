from django.conf.urls import url
import views

contest_patterns = [
    url(r'^acl_test/(?P<acl_id>\d+)/$', views.evaluate)
]
