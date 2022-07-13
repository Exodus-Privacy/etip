from rest_framework import serializers

from trackers.models import Tracker, TrackerCategory


class TrackerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackerCategory
        fields = ['name']


class TrackerSerializer(serializers.ModelSerializer):
    category = TrackerCategorySerializer(read_only=True, many=True)
    documentation = serializers.ListField(source='documentation_list')

    class Meta:
        model = Tracker
        fields = [
          'id',
          'name',
          'category',
          'description',
          'documentation',
          'is_in_exodus',
          'code_signature',
          'network_signature',
          'api_key_ids',
          'website',
          'maven_repository',
          'group_id',
          'artifact_id',
          'gradle',
          'created',
          'updated',
          'creation_date',
          'capability',
          'advertising',
          'analytic',
          'network',
          'comments',
          'exodus_matches',
          'needs_rework',
        ]
        depth = 1
