from rest_framework import viewsets
from rest_framework.decorators import authentication_classes, permission_classes

from restful_api.serializers import TrackerSerializer
from trackers.models import Tracker


@authentication_classes(())
@permission_classes(())
class TrackerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows trackers to be viewed or edited.
    """
    queryset = Tracker.objects.all().order_by('name')
    serializer_class = TrackerSerializer
