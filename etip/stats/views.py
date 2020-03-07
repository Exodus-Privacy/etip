from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from trackers.models import Tracker


@login_required
def index(request):
    trackers = Tracker.objects.all()

    if trackers.count() == 0:
        return JsonResponse({})

    trackers_in_exodus = trackers.filter(is_in_exodus=True)
    trackers_only_in_etip = trackers.filter(is_in_exodus=False)

    trackers_with_collisions = list(
        t for t in trackers if t.has_any_signature_collision()
    )

    last_week = timezone.now() - timedelta(days=7)
    trackers_from_last_week = trackers.filter(created__gte=last_week)

    last_month = timezone.now() - timedelta(days=30)
    trackers_from_last_month = trackers.filter(created__gte=last_month)

    latest_updated = trackers.order_by('-updated').first()

    data = {
        'trackers': {
            'all': trackers.count(),
            'in_exodus': trackers_in_exodus.count(),
            'only_in_etip': trackers_only_in_etip.count(),
            'with_collisions': len(trackers_with_collisions),
            'latest_update_time': latest_updated.updated,
            'added': {
                'last_week': trackers_from_last_week.count(),
                'last_month': trackers_from_last_month.count(),
            },
        }
    }

    return JsonResponse(data)
