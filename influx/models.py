from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from oioioi.questions.models import Message
from oioioi.programs.models import Submission
from datetime import datetime
from django.contrib.sites.models import Site
from influxdb import InfluxDBClient

class InfluxClient:
    def __init__(self, host, port, database):
        self.host, self.port, self.database = host, port, database

    def __enter__(self):
        self.client = InfluxDBClient(host=self.host, port=self.port, database=self.database, username='monitoring', password='alamakota', timeout=3)
        return self

    def __exit__(self, *args):
        pass

    def append(self, time, data, kind):
        if self.client is None: return
        data = {
            'measurement': kind,
            'tags': {'source': 'influx@sio2'},
            'time': time,
            'fields': data
        }
        self.client.write_points([data])



#@receiver(post_save, sender=Message)
def question(sender, instance, created, **kwargs):
    return
    if created:
        time = datetime.now()
        data = {
            'author': instance.author.first_name+' '+instance.author.last_name,
            'title': instance.topic,
            'contest': instance.problem.contest.name,
            'link': '<a href="'+l+'">link</a>'
        }
        with InfluxClient('10.14.71.2', 18086, 'monitoring') as ic:
            ic.append(time, data, 'question')


#@receiver(post_save, sender=Submission)
def submission(sender, instance, created, **kwargs):
    time = datetime.now()
    data = {
        'author': instance.user.first_name+' '+instance.user.last_name,
        'id': instance.id,
        'contest': instance.contest.name,
        'status': instance.status,
    }
    with InfluxClient('10.14.71.2', 18086, 'monitoring') as ic:
        ic.append(time, data, 'submission')
