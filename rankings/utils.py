from django.contrib.admin import TabularInline, StackedInline

def inline_for(inline_type, model, ranking_type):
    return type(model._meta.model_name + 'Inline', (inline_type, ), dict(model=model, ranking_type=ranking_type.type_id))

def stacked_inline_for(*args, **kwargs):
    return inline_for(StackedInline, *args, **kwargs)

def tabular_inline_for(*args, **kwargs):
    return inline_for(TabularInline, *args, **kwargs)
