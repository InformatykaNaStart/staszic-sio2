from django.conf.urls import patterns, include, url
import views

urlpatterns = [url(r'^s/(\d+)/(\d+)/model/$', views.showmodel_view, name='showmodel')]
