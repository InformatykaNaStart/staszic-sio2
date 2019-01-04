from django.shortcuts import render
from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.utils.safestring import mark_safe
import os.path
import markdown
import codecs

def doc(request, doc):
    try:
        md = codecs.open(os.path.expanduser('~/docs/'+doc+'.md'), encoding='utf-8').read()
    except IOError:
        raise Http404
    return render(request, 'docs/doc.html', {'doc': mark_safe(markdown.markdown(md)), 'title':doc})
