from django.conf.urls import url
import views

contest_patterns = [
    url(r'^re/(\d+)/$', views.re_view, name='python-re'),
]

