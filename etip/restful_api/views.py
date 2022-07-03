from rest_framework import viewsets

from restful_api.serializers import TrackerSerializer
from trackers.models import Tracker


class TrackerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows trackers to be viewed or edited.
    """
    queryset = Tracker.objects.all().order_by('name')
    serializer_class = TrackerSerializer
