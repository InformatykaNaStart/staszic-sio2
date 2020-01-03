from django.conf.urls import url
import views

noncontest_patterns = [
    url(r'ctf/$', views.ctf_view, name='ctf_view'),
    url(r'staszic/pool/$', views.pool_info, name='staszic-pool-info'),
    url(r'staszic/pool/up/$', views.pool_sign, name='staszic-pool-up'),
    url(r'staszic/pool/down/$', views.pool_unsign, name='staszic-pool-down'),
    url(r'staszic/pool/bl/ins$', views.pool_bl_ins, name='staszic-bl-ins'),
    url(r'staszic/pool/bl/del(?P<id>\d+)$', views.pool_bl_del, name='staszic-bl-del'),
]
