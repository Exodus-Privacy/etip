from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from trackers.models import Tracker, TrackerCategory


class RestfulApiGetAllTrackersTests(APITestCase):

    TRACKERS_PATH = '/api/trackers/'

    def force_autentication(self):
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)

    def test_get_unauthorized_when_no_auth(self):
        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_empty_when_no_tracker(self):
        self.force_autentication()
        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_trackers_with_details_without_documentation(self):
        self.force_autentication()

        tracker = Tracker.objects.create(
            name='tracker1',
            description='description of the tracker',
            code_signature='com.tracker1.ads',
            network_signature='tracker1.com',
            website='https://tracker1.com',
            is_in_exodus=True,
            maven_repository='https://jcenter.bintray.com/',
            group_id='com.tracker1',
            artifact_id='tracker',
            gradle='com.tracker1:tracker:1.2.3',
        )

        category1 = TrackerCategory.objects.create(name='Ads')
        category2 = TrackerCategory.objects.create(name='Location')
        tracker.category.add(category1)
        tracker.category.add(category2)
        self.maxDiff = None
        expected_tracker = [{
            'id': str(tracker.id),
            'name': tracker.name,
            'description': tracker.description,
            'code_signature': tracker.code_signature,
            'network_signature': tracker.network_signature,
            'website': tracker.website,
            'documentation': [],
            'is_in_exodus': tracker.is_in_exodus,
            'category': [{'name': 'Ads'}, {'name': 'Location'}],
            'maven_repository': tracker.maven_repository,
            'group_id': tracker.group_id,
            'artifact_id': tracker.artifact_id,
            'gradle': tracker.gradle,
        }]

        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json(), expected_tracker)

    def test_get_trackers_with_details(self):
        self.force_autentication()

        tracker = Tracker.objects.create(
            name='tracker1',
            description='description of the tracker',
            code_signature='com.tracker1.ads',
            network_signature='tracker1.com',
            website='https://tracker1.com',
            is_in_exodus=True,
            maven_repository='https://jcenter.bintray.com/',
            group_id='com.tracker1',
            artifact_id='tracker',
            gradle='com.tracker1:tracker:1.2.3',
            documentation='https://t1.com http://t1.com/doc'
        )

        category1 = TrackerCategory.objects.create(name='Ads')
        category2 = TrackerCategory.objects.create(name='Location')
        tracker.category.add(category1)
        tracker.category.add(category2)
        self.maxDiff = None
        expected_tracker = [{
            'id': str(tracker.id),
            'name': tracker.name,
            'description': tracker.description,
            'code_signature': tracker.code_signature,
            'network_signature': tracker.network_signature,
            'website': tracker.website,
            'documentation': ['https://t1.com', 'http://t1.com/doc'],
            'is_in_exodus': tracker.is_in_exodus,
            'category': [{'name': 'Ads'}, {'name': 'Location'}],
            'maven_repository': tracker.maven_repository,
            'group_id': tracker.group_id,
            'artifact_id': tracker.artifact_id,
            'gradle': tracker.gradle,
        }]

        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json(), expected_tracker)

    def test_get_trackers_when_2(self):
        self.force_autentication()

        Tracker.objects.create(name='toto')
        Tracker.objects.create(name='toto2')

        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_is_not_allowed(self):
        self.force_autentication()
        response = self.client.post(self.TRACKERS_PATH)

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_is_not_allowed(self):
        self.force_autentication()
        response = self.client.put(self.TRACKERS_PATH)

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_is_not_allowed(self):
        self.force_autentication()
        response = self.client.delete(self.TRACKERS_PATH)

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
