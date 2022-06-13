from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from oioioi.questions.models import Message
from oioioi.programs.models import Submission
from datetime import datetime
from django.contrib.sites.models import Site
from influxdb import InfluxDBClient
from django.conf import settings

class InfluxClient:
    def __init__(self, host=settings.INFLUX_IP, port=settings.INFLUX_PORT, database=settings.INFLUX_DB):
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
