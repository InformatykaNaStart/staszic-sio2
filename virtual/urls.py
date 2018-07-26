from django.conf.urls import url
import views

urlpatterns = [
    url(r'^virtual/$', views.virtual, name='virtual-contests'),
    url(r'^virtual/(?P<vcontest_id>\d+)/$', views.info, name='virtual-info'),
    url(r'^virtual/(?P<vcontest_id>\d+)/start/$', views.start, name='virtual-start'),
    url(r'^virtual/(?P<vcontest_id>\d+)/finish/$', views.finish, name='virtual-finish'),
]
