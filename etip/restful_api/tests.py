from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from trackers.models import Advertising, Tracker, TrackerCategory


class RestfulApiGetAllTrackersTests(APITestCase):

    TRACKERS_PATH = '/api/trackers/'
    TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'  # ISO8601

    def test_get_empty_when_no_tracker(self):
        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_trackers_with_details_without_documentation(self):

        tracker = Tracker.objects.create(
            name='tracker1',
            description='description of the tracker',
            code_signature='com.tracker1.ads',
            network_signature='tracker1.com',
            api_key_ids='ga_trackingId',
            website='https://tracker1.com',
            is_in_exodus=True,
            maven_repository='https://jcenter.bintray.com/',
            group_id='com.tracker1',
            artifact_id='tracker',
            gradle='com.tracker1:tracker:1.2.3',
            comments='this is a test',
            exodus_matches=0,
            needs_rework=True,
        )

        category1 = TrackerCategory.objects.create(name='Ads')
        category2 = TrackerCategory.objects.create(name='Location')
        tracker.category.add(category1)
        tracker.category.add(category2)
        expected_tracker = [{
            'id': str(tracker.id),
            'name': tracker.name,
            'description': tracker.description,
            'code_signature': tracker.code_signature,
            'network_signature': tracker.network_signature,
            'api_key_ids': tracker.api_key_ids,
            'website': tracker.website,
            'documentation': [],
            'is_in_exodus': tracker.is_in_exodus,
            'category': [{'name': 'Ads'}, {'name': 'Location'}],
            'maven_repository': tracker.maven_repository,
            'group_id': tracker.group_id,
            'artifact_id': tracker.artifact_id,
            'gradle': tracker.gradle,
            'created': tracker.created.strftime(self.TIME_FORMAT),
            'updated': tracker.updated.strftime(self.TIME_FORMAT),
            'creation_date': date.today().isoformat(),
            'capability': [],
            'advertising': [],
            'analytic': [],
            'network': [],
            'comments': tracker.comments,
            'exodus_matches': tracker.exodus_matches,
            'needs_rework': tracker.needs_rework,
        }]

        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json(), expected_tracker)

    def test_get_trackers_with_details(self):

        tracker = Tracker.objects.create(
            name='tracker1',
            description='description of the tracker',
            code_signature='com.tracker1.ads',
            network_signature='tracker1.com',
            api_key_ids='foo,bar',
            website='https://tracker1.com',
            is_in_exodus=True,
            maven_repository='https://jcenter.bintray.com/',
            group_id='com.tracker1',
            artifact_id='tracker',
            gradle='com.tracker1:tracker:1.2.3',
            documentation='https://t1.com http://t1.com/doc',
            comments='',
            exodus_matches=29,
            needs_rework=False,
        )

        category1 = TrackerCategory.objects.create(name='Ads')
        category2 = TrackerCategory.objects.create(name='Location')
        tracker.category.add(category1)
        tracker.category.add(category2)

        # use fake names so tests work without syncing the db with Exodus
        ad_name = 'fake ad type name'
        ad = Advertising.objects.create(name=ad_name)
        tracker.advertising.add(ad)
        created = ad.serializable_value('created').strftime(self.TIME_FORMAT)
        updated = ad.serializable_value('updated').strftime(self.TIME_FORMAT)

        expected_tracker = [{
            'id': str(tracker.id),
            'name': tracker.name,
            'description': tracker.description,
            'code_signature': tracker.code_signature,
            'network_signature': tracker.network_signature,
            'api_key_ids': tracker.api_key_ids,
            'website': tracker.website,
            'documentation': ['https://t1.com', 'http://t1.com/doc'],
            'is_in_exodus': tracker.is_in_exodus,
            'category': [{'name': 'Ads'}, {'name': 'Location'}],
            'maven_repository': tracker.maven_repository,
            'group_id': tracker.group_id,
            'artifact_id': tracker.artifact_id,
            'gradle': tracker.gradle,
            'created': tracker.created.strftime(self.TIME_FORMAT),
            'updated': tracker.updated.strftime(self.TIME_FORMAT),
            'creation_date': date.today().isoformat(),
            'capability': [],
            'advertising': [
                {
                    'id': str(ad.serializable_value('id')),
                    'name': ad_name,
                    'created': created,
                    'updated': updated,
                    'description': '',
                    'is_in_exodus': False,
                }
            ],
            'analytic': [],
            'network': [],
            'comments': tracker.comments,
            'exodus_matches': tracker.exodus_matches,
            'needs_rework': tracker.needs_rework,
        }]

        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json(), expected_tracker)

    def test_get_trackers_when_2(self):

        Tracker.objects.create(name='toto')
        Tracker.objects.create(name='toto2')

        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_is_not_allowed(self):
        response = self.client.post(self.TRACKERS_PATH)

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_is_not_allowed(self):
        response = self.client.put(self.TRACKERS_PATH)

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_is_not_allowed(self):
        response = self.client.delete(self.TRACKERS_PATH)

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
