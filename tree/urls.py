from django.conf.urls import url
import views

noncontest_patterns = [
    url(r'^tree/$', views.contests_tree_view, name='contests-tree'),
]
