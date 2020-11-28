from django.http import JsonResponse
from django.http.response import Http404
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError, PermissionDenied

from .models import Tracker, TrackerApproval

import reversion


def home(request):
    return render(request, 'home.html')


def index(request):
    try:
        # TODO: Use a Django Form instead ?
        filter_name = request.GET.get('tracker_name', '')
        only_collisions = request.GET.get('only_collisions', False)
        approve_select = request.GET.get('approve_select', '')
        trackers_select = request.GET.get('trackers_select', '')
        if filter_name:
            trackers = Tracker.objects.filter(name__startswith=filter_name)
        else:
            trackers = Tracker.objects

        trackers = trackers.order_by('name')

        if trackers_select == "exodus":
            trackers = trackers.filter(is_in_exodus=True)
        elif trackers_select == "etip":
            trackers = trackers.filter(is_in_exodus=False)

        if only_collisions:
            trackers = list(
                t for t in trackers if t.has_any_signature_collision()
            )

        if approve_select == "approved":
            trackers = list(
                t for t in trackers if t.approvals.count() >= 2
            )
        elif approve_select == "need_review":
            trackers = list(
                t for t in trackers if t.approvals.count() == 1
            )
        elif approve_select == "no_approvals":
            trackers = list(
                t for t in trackers if t.approvals.count() == 0
            )

        count = len(trackers)

        paginator = Paginator(trackers, 20)
        page = request.GET.get('page', 1)
        trackers = paginator.get_page(page)
    except Tracker.DoesNotExist:
        raise Http404("trackers does not exist")

    return render(request, 'tracker_list.html', {
        'trackers': trackers,
        'count': count,
        'filter_name': filter_name,
        'only_collisions': 'checked' if only_collisions else '',
        'approve_select': approve_select,
        'trackers_select': trackers_select
    })


def display_tracker(request, id):
    try:
        tracker = Tracker.objects.get(pk=id)
    except (Tracker.DoesNotExist, ValidationError):
        raise Http404("Tracker does not exist")

    return render(request, 'tracker.html', {'tracker': tracker})


def review(request):
    try:
        trackers = Tracker.objects.filter(is_in_exodus=False).order_by('name')
        trackers = list(t for t in trackers if t.approvals.count() == 1)

        count = len(trackers)

        paginator = Paginator(trackers, 20)
        page = request.GET.get('page', 1)
        trackers = paginator.get_page(page)
    except Tracker.DoesNotExist:
        raise Http404("trackers does not exist")

    return render(request, 'tracker_review.html', {
        'title': 'Waiting for review',
        'trackers': trackers,
        'count': count,
    })


def approved(request):
    try:
        trackers = Tracker.objects.filter(is_in_exodus=False).order_by('name')
        trackers = list(t for t in trackers if t.approvals.count() >= 2)

        count = len(trackers)

        paginator = Paginator(trackers, 20)
        page = request.GET.get('page', 1)
        trackers = paginator.get_page(page)
    except Tracker.DoesNotExist:
        raise Http404("trackers does not exist")

    return render(request, 'tracker_review.html', {
        'title': 'Approved trackers',
        'trackers': trackers,
        'count': count,
    })


def export_tracker_list(request):
    trackers = Tracker.objects.order_by('name')
    trackers_list = list(trackers.values(*Tracker.EXPORTABLE_FIELDS))
    response = JsonResponse(dict(trackers=trackers_list))
    response['Content-Disposition'] = 'attachment; filename=trackers.json'
    return response


def approve(request, id):
    if request.method != 'POST':
        return redirect('/')

    if not request.user.is_authenticated:
        raise PermissionDenied

    try:
        tracker = Tracker.objects.get(pk=id)
    except (Tracker.DoesNotExist, ValidationError):
        raise Http404("Tracker does not exist")

    if tracker.creator() and request.user == tracker.creator():
        raise PermissionDenied

    approval = TrackerApproval(
        tracker=tracker,
        approver=request.user
    )
    approval.save()
    return redirect('/trackers/{}'.format(tracker.id))


def revoke(request, id):
    if request.method != 'POST':
        return redirect('/')

    if not request.user.is_authenticated:
        raise PermissionDenied

    try:
        tracker = Tracker.objects.get(pk=id)
    except (Tracker.DoesNotExist, ValidationError):
        raise Http404("Tracker does not exist")

    approval = TrackerApproval.objects.get(
        tracker=tracker,
        approver=request.user
    )
    approval.delete()
    return redirect('/trackers/{}'.format(tracker.id))


def ship(request, id):
    if request.method != 'POST':
        return redirect('/')

    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied

    try:
        tracker = Tracker.objects.get(pk=id)
    except (Tracker.DoesNotExist, ValidationError):
        raise Http404("Tracker does not exist")

    with reversion.create_revision():
        tracker.is_in_exodus = True
        tracker.save()

        reversion.set_user(request.user)
        reversion.set_comment("Shipped to exodus")

    return redirect('/trackers/{}'.format(tracker.id))
