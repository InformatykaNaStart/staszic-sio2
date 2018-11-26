from django.conf.urls import url
import views

urlpatterns = [
    url(r'^queue/queue.txt$', views.get_queue_ajax, name='show_queue_txt'),
]
