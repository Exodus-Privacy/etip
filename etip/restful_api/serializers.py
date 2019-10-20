from trackers.models import Tracker
from rest_framework import serializers


class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = [
          'name',
          'category',
          'description',
          'is_in_exodus',
          'code_signature',
          'network_signature',
          'website'
        ]
        depth = 1
