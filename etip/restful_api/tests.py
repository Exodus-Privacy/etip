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

    def test_get_trackers_with_details(self):
        self.force_autentication()

        tracker = Tracker.objects.create(
            name='tracker1',
            description='description of the tracker',
            code_signature='com.tracker1.ads',
            network_signature='tracker1.com',
            website='https://tracker1.com',
            is_in_exodus=True,
        )

        category1 = TrackerCategory.objects.create(name='Ads')
        category2 = TrackerCategory.objects.create(name='Location')
        tracker.category.add(category1)
        tracker.category.add(category2)

        expected_tracker = [{
            'name': 'tracker1',
            'description': 'description of the tracker',
            'code_signature': 'com.tracker1.ads',
            'network_signature': 'tracker1.com',
            'website': 'https://tracker1.com',
            'is_in_exodus': True,
            'category': [{'name': 'Ads'}, {'name': 'Location'}]
        }]

        response = self.client.get(self.TRACKERS_PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json(), expected_tracker)

    def test_get_trackers_when_2(self):
        self.force_autentication()

        Tracker.objects.create()
        Tracker.objects.create()

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
