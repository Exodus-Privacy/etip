from rest_framework import viewsets
from trackers.models import Tracker
from restful_api.serializers import TrackerSerializer


class TrackerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows trackers to be viewed or edited.
    """
    queryset = Tracker.objects.all().order_by('name')
    serializer_class = TrackerSerializer
