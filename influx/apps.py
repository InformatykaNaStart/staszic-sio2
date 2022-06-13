from __future__ import unicode_literals

from django.apps import AppConfig


class InfluxConfig(AppConfig):
    name = 'influx'
    def ready(self):
        import signals
        raise RuntimeError()
