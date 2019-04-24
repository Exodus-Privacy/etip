from django.http import JsonResponse
from django.http.response import Http404
from django.core.paginator import Paginator
from django.shortcuts import render

from trackers.models import Tracker


def index(request):
    try:
        filter_name = request.GET.get('tracker_name', '')
        if filter_name:
            trackers = Tracker.objects.filter(name__startswith=filter_name)
        else:
            trackers = Tracker.objects

        trackers = trackers.order_by('name')
        count = trackers.count()

        paginator = Paginator(trackers, 20)
        page = request.GET.get('page', 1)
        trackers = paginator.page(page)
    except Tracker.DoesNotExist:
        raise Http404("trackers does not exist")

    return render(request, 'tracker_list.html', {
        'trackers': trackers,
        'count': count,
        'filter_name': filter_name
    })


def export_tracker_list(request):
    trackers = Tracker.objects.order_by('name')
    trackers_list = list(trackers.values(*Tracker.EXPORTABLE_FIELDS))
    response = JsonResponse(dict(trackers=trackers_list))
    response['Content-Disposition'] = 'attachment; filename=trackers.json'
    return response
