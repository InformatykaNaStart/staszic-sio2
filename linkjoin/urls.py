from django.conf.urls import url

import views

noncontest_patterns = [
    url(r'^join/(?P<magic>[a-z0-9]+)$', views.linkjoin_view, name='link-join'),
]
