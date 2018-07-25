from django.conf.urls import url
import views

contest_patterns = [
    url(r'^r/$', views.ranking_view, name='default-ranking'),
    url(r'^r/(?P<ranking_id>\d+)/$', views.ranking_view, name='ranking'),
]
