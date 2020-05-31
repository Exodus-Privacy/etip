from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from trackers.models import Tracker


class IndexStatsListViewTests(TestCase):
    PATH = reverse('stats:index')

    def _force_authentication(self, c):
        c.user = User.objects.create_user('jane', 'jdoe@mail.com', '@password')
        c.login(username='jane', password='@password')

    def test_redirects_if_not_logged_in(self):
        c = Client()

        response = c.get(self.PATH)

        login_url = "{}?next={}".format(settings.LOGIN_URL, self.PATH)
        self.assertRedirects(response, login_url)

    def test_get_empty_json_if_no_data(self):
        c = Client()
        self._force_authentication(c)

        response = c.get(self.PATH)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_get_total_trackers_count(self):
        c = Client()
        self._force_authentication(c)

        Tracker.objects.create(
            name='tracker 1',
            code_signature='toto.com',
            network_signature='network.signature',
            website='https://website1'
        )
        Tracker.objects.create(
            name='tracker 2',
            code_signature='code_2',
            network_signature='other.signature',
            website='https://website2'
        )

        response = c.get(self.PATH)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['trackers']['all'], 2)
        self.assertEqual(response.json()['trackers']['with_collisions'], 0)

    def test_get_in_exodus_trackers_count(self):
        c = Client()
        self._force_authentication(c)

        Tracker.objects.create(
            name='tracker 1',
            code_signature='toto.com',
            network_signature='network.signature1',
            is_in_exodus=True
        )
        Tracker.objects.create(
            name='tracker 2',
            code_signature='code_2',
            network_signature='network.signature2',
            is_in_exodus=True
        )
        Tracker.objects.create(
            name='tracker 3',
            code_signature='code_3',
            network_signature='network.signature3',
            is_in_exodus=False
        )

        response = c.get(self.PATH)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['trackers']['all'], 3)
        self.assertEqual(response.json()['trackers']['in_exodus'], 2)
        self.assertEqual(response.json()['trackers']['only_in_etip'], 1)

    def test_get_trackers_with_collisions(self):
        c = Client()
        self._force_authentication(c)

        Tracker.objects.create(
            name="toto",
            network_signature="toto.com.truc",
        )
        Tracker.objects.create(
            name="tutu",
            network_signature="toto.com",
        )
        Tracker.objects.create(
            name="toto2",
            network_signature="tata.com",
            code_signature="titi.com"
        )
        Tracker.objects.create(
            name="tutu2",
            network_signature="titi.com",
            code_signature="tata.com"
        )

        response = c.get(self.PATH)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['trackers']['with_collisions'], 1)
