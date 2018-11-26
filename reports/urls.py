from django.conf.urls import url
import views

contest_patterns = [
    url(r'^report_modal/(\d+)/$', views.report_modal_view, name='report-modal'),
    url(r'^info_button/(\d+)/$', views.info_button_view, name='report-info-button'),
]
