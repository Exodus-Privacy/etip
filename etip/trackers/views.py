from django.http import JsonResponse
from django.http.response import Http404
from django.core.paginator import Paginator
from django.shortcuts import render

from trackers.models import Tracker


def index(request):
    try:
        trackers = Tracker.objects.order_by('name')
        count = trackers.count()

        paginator = Paginator(trackers, 20)
        page = request.GET.get('page', 1)
        trackers = paginator.page(page)
    except Tracker.DoesNotExist:
        raise Http404("trackers does not exist")

    return render(request, 'tracker_list.html', {
        'trackers': trackers,
        'count': count
    })


def export_tracker_list(request):
    trackers = Tracker.objects.order_by('name')
    trackers_list = list(trackers.values(*Tracker.EXPORTABLE_FIELDS))
    response = JsonResponse(dict(trackers=trackers_list))
    response['Content-Disposition'] = 'attachment; filename=trackers.json'
    return response
