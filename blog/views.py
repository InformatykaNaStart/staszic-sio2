from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from oioioi.base.permissions import not_anonymous, make_request_condition
from oioioi.base.main_page import register_main_page_view

@make_request_condition
def is_anonymous(request):
    return (not request.user.is_authenticated())

@register_main_page_view(order=100)
def blog_view(request):
    return render(request, 'blog/main.html', {})
