from django.conf.urls import url
import views

contest_patterns = [
    url(r'^r/$', views.ranking_view, name='default-ranking'),
    url(r'^r/(?P<ranking_id>\d+)/$', views.ranking_view, name='ranking'),
    url(r'^r/(?P<ranking_id>\d+)/flush$', views.cache_flush_view, name='ranking_cache_flush'),
    url(r'^r/(?P<ranking_id>\d+)/csv$', views.csv_view, name='ranking_csv'),
]
