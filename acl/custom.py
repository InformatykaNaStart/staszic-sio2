from django.forms import Textarea
from django.template import loader
import json

    

class RulesetWidget(Textarea):
    class Media:
        css = { 'all': [ 'acl/style.css' ] }
        js = [ 'acl/script.js' ]

    def render(self, *args, **kwargs):
        from acl_rules import ACLRuleBase
        base_widget = super(RulesetWidget, self).render(*args, **kwargs)

        config = ACLRuleBase.make_all_config()

        return loader.render_to_string('acl/ruleset_widget.html', dict(
            base_widget=base_widget,
            config=json.dumps(config)
        ))
