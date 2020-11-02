from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from oioioi.contests.models import Contest
from django.core.urlresolvers import reverse
from oioioi.base.utils import make_html_link
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import random


def random_link():
    charset = 'abcdefghijkmnpqrstuvwxyz23456789'
    length = settings.JOINLINK_LENGTH
    magic = ''.join([random.choice(charset) for i in range(length)])
    return magic


def generate_link():
    l = random_link()
    while (Link.objects.filter(magic=l).exists()):
        l = random_link()
    return l

class Link(models.Model):
    contest = models.ForeignKey(Contest)
    magic = models.CharField(verbose_name='ID', max_length=256, unique=True, default=generate_link, editable=False)
    expiration_date = models.DateTimeField(verbose_name=_('Expiration date'), null=True, blank=True)
    comment = models.CharField(verbose_name=_('Comment'), max_length=64, null=True, blank=True)
    active = models.BooleanField(verbose_name=_('Link active'), default=True)

    def link(self):
        path = reverse('link-join', args=[self.magic])
        domain = Site.objects.get_current().domain
        return domain + path

class LinkClickHistory(models.Model):
    user = models.OneToOneField(User)
    last_click = models.DateTimeField(null=True, blank=True)