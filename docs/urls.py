from django.conf.urls import url
import views

noncontest_patterns = [
    url(r'^docs/([a-z0-9_-]+)$', views.doc, name='doc'),
]
