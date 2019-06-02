from django.shortcuts import render
import policy

def blocked_view(request):
        return render(request, 'antiddos/blocked.html', {'limit': policy.get_queued_submissions_limit()})
