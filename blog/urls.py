from django.conf.urls import url
import views

noncontest_patterns = [
    url(r'^blog/$', views.blog_view, name='blog'),
]
