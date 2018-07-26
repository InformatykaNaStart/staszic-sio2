from django.conf.urls import patterns, include, url
import views

contest_patterns = [url(r'^s/(\d+)/edit/$', views.edit_view, name='edit_results')]

