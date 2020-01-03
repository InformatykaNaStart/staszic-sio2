from django.conf.urls import url
import views

noncontest_patterns = [
    url(r'^stats/timing$', views.timing_view, name='timing'),
]

contest_patterns = [
    url(r'^stats/submissions$', views.submissions_view, name='submissions'),
]
