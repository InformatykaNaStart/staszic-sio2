from django.contrib.admin import TabularInline, StackedInline

def inline_for(inline_type, model, ranking_type, extra={}):
    extra.update( dict(model=model, ranking_type=ranking_type.type_id))
    extra.update( dict(has_change_permission=(lambda *args, **kwargs: True)) )
    return type(model._meta.model_name + 'Inline', (inline_type, ), extra)

def stacked_inline_for(*args, **kwargs):
    return inline_for(StackedInline, *args, **kwargs)

def tabular_inline_for(*args, **kwargs):
    return inline_for(TabularInline, *args, **kwargs)
