from __future__ import unicode_literals

from oioioi.contests.models import Contest
from django.db import models
import json
from acl_rules import ACLRuleBase
from django.contrib.contenttypes.models import ContentType

class ACLOutcome:
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'
    DEFAULT = 'DEFAULT'
    ERROR = 'ERROR'

class ACL(models.Model):
    contest = models.ForeignKey(Contest)
    name = models.CharField(max_length=100)
    json_ruleset = models.TextField(default='[]')

    @property
    def ruleset(self):
        parsed_json = json.loads(self.json_ruleset)
        return parsed_json
        
    def evaluate(self, request):
        idx = 0
        rules = self.ruleset
        visited = set()

        while idx < len(rules) and idx not in visited:
            visited.add(idx)
            rule = rules[idx]
            rule_instance = ACLRuleBase.instance_of(rule['type'])

            if rule_instance.evaluate(request, rule):
                if rule['action'] == 'ACCEPT': return ACLOutcome.ACCEPT
                elif rule['action'] == 'REJECT': return ACLOutcome.REJECT
                elif rule['action'] == 'DEFAULT': return ACLOutcome.DEFAULT
                elif rule['action'] == 'GOTO': idx = int(rule['goto_label']) - 1
                else: return ACLOutcome.ERROR
            else:
                idx += 1
            

        if idx == len(rules): return ACLOutcome.DEFAULT
        return ACLOutcome.ERROR

    def __unicode__(self):
        return self.name

class ACLHook(models.Model):
    model = models.ForeignKey(ContentType)
    object_id = models.TextField()
    action = models.CharField(max_length=16)
    acl = models.ForeignKey(ACL)

    class Meta:
        unique_together = ['model', 'object_id', 'action']

    def get_object(self):
        return self.model.get_object_for_this_type(pk=self.object_id)
