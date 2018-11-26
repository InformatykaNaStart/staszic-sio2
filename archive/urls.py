from django.conf.urls import url
import views
#import staszic.timetable.views

noncontest_patterns = [
    url(r'^archive/$', views.home_view, name='archive-home'),
    #url(r'^plan/$', staszic.timetable.views.tt_view, name='timetable'),
    url(r'^archive/([a-z0-9_-]+)/s$', views.submissions_view, name='archive-submissions'),
    url(r'^archive/([a-z0-9_-]+)/p$', views.problems_view, name='archive-problems'),
    url(r'^archive/sio2dead/([a-z0-9_-]+)/p$', views.problems_sio2dead_view, name='archive-sio2dead-problems'),
    url(r'^archive/([a-z0-9_-]+)/all_s$', views.all_submissions_view, name='archive-submissions-all'),
    url(r'^archive/[a-z0-9_-]+/(\d+)/package', views.download_package_view, name='archive-package'),
    url(r'^archive/([a-z0-9_-]+)/(\d+)/statement/$', views.statement_view, name='archive-statement'),
    url(r'^archive/([a-z0-9_-]+)/(\d+)/statement/(.+)$', views.zip_view, name='archive-statement-zip'),
    url(r'^archive/source/(\d+)/$', views.download_source_code_view, name='archive-code'),

]
