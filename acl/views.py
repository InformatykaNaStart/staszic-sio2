from django.shortcuts import render, get_object_or_404
from models import ACL
from django.http import HttpResponse


def evaluate(request, acl_id):
    acl = get_object_or_404(ACL, pk=acl_id)
    return HttpResponse(str(acl.evaluate(request)))
