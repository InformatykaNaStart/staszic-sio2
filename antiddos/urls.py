from django.conf.urls import url
import views

noncontest_patterns = [
    url(r'^blocked_submission/$', views.blocked_view, name='blocked_submission'),
]
