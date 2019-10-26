from trackers.models import Tracker, TrackerCategory
from rest_framework import serializers


class TrackerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackerCategory
        fields = ['name']


class TrackerSerializer(serializers.ModelSerializer):
    category = TrackerCategorySerializer(read_only=True, many=True)

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
