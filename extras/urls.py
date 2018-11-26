from django.conf.urls import url

import views

contest_patterns = [
    url(r'^staszic/extras/$', views.staszic_extras, name='staszic-extras'),
    url(r'^staszic/extras/rejudge$', views.doesnt_need, name='staszic-doesnt-need-rejudge'),
    url(r'^staszic/extras/statement$', views.change_statement, name='staszic-change-statement'),
    url(r'^staszic/extras/limit$', views.change_sub_limit, name='staszic-sub-limit'),
]
