from django.test import TestCase, Client
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from .models import \
    Tracker, Capability, Advertising, Analytic, Network, TrackerCategory
from io import BytesIO, StringIO
from unittest.mock import patch


class TrackerModelTests(TestCase):

    def test_clean_fields_with_incorrect_code_signature(self):
        tracker = Tracker(
            name="tracker1",
            website="http://example.com",
            code_signature="*com.tracker.code"
        )

        with self.assertRaisesRegexp(ValidationError, "Must be a valid regex"):
            tracker.full_clean()

    def test_clean_fields_without_code_signature(self):
        tracker = Tracker(
            name="tracker1",
            website="http://example.com"
        )

        try:
            tracker.full_clean()
        except ValidationError:
            self.fail("full_clean() raised unexpectedly")

    def test_clean_fields_with_correct_code_signature(self):
        tracker = Tracker(
            name="tracker1",
            website="http://example.com",
            code_signature="com.tracker.code"
        )

        try:
            tracker.full_clean()
        except ValidationError:
            self.fail("full_clean() raised unexpectedly")

    def test_any_signature_collision_with_code_signature_one(self):
        existing_tracker = Tracker(
            name="toto",
            code_signature="toto.com",
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="tutu",
            code_signature="toto.com",
        )
        new_tracker.save()
        self.assertEquals(new_tracker.has_any_signature_collision(), True)

    def test_any_signature_collision_with_network_signature_one(self):
        existing_tracker = Tracker(
            name="toto",
            network_signature="toto.com",
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="tutu",
            network_signature="toto.com",
        )
        new_tracker.save()
        self.assertEquals(new_tracker.has_any_signature_collision(), True)

    def test_any_signature_collision_containing_network_signature_one(self):
        existing_tracker = Tracker(
            name="toto",
            network_signature="toto.com.truc",
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="tutu",
            network_signature="toto.com",
        )
        new_tracker.save()
        self.assertEquals(new_tracker.has_any_signature_collision(), True)

    def test_any_signature_collision_without_collisions(self):
        existing_tracker = Tracker(
            name="toto",
            network_signature="tata.com",
            code_signature="titi.com"
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="tutu",
            network_signature="titi.com",
            code_signature="tata.com"
        )
        new_tracker.save()
        self.assertEquals(new_tracker.has_any_signature_collision(), False)

    def test_code_collision_different_signature(self):
        existing_tracker = Tracker(
            name="toto",
            code_signature="toto.com",
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="tutu",
            code_signature="tutu.com",
        )
        new_tracker.save()
        collisions = \
            new_tracker.get_trackers_with_code_signature_collision()
        self.assertEquals(collisions, [])

    def test_code_collision_same_signature(self):
        existing_tracker_name = "toto"
        signature = "toto.com"
        existing_tracker = Tracker(
            name=existing_tracker_name,
            code_signature=signature,
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="toto2",
            code_signature=signature,
        )
        new_tracker.save()
        collisions = new_tracker.get_trackers_with_code_signature_collision()
        self.assertEquals(collisions, [existing_tracker_name])

    def test_network_collision_same_signature(self):
        existing_tracker_name = "toto"
        signature = "toto.com"
        existing_tracker = Tracker(
            name=existing_tracker_name,
            network_signature=signature,
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="toto2",
            network_signature=signature,
        )
        new_tracker.save()
        collisions = \
            new_tracker.get_trackers_with_network_signature_collision()
        self.assertEquals(collisions, [existing_tracker_name])

    def test_network_collision_contains_signature(self):
        existing_tracker_name = "toto"
        signature = "toto.com"
        existing_tracker = Tracker(
            name=existing_tracker_name,
            network_signature=signature + '/test',
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="toto2",
            network_signature=signature,
        )
        new_tracker.save()
        collisions = \
            new_tracker.get_trackers_with_network_signature_collision()
        self.assertEquals(collisions, [existing_tracker_name])

    def test_code_collision_contains_signature(self):
        existing_tracker_name = "toto"
        signature = "toto.com"
        existing_tracker = Tracker(
            name=existing_tracker_name,
            code_signature=signature + '/test',
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="toto2",
            code_signature=signature,
        )
        new_tracker.save()
        collisions = new_tracker.get_trackers_with_code_signature_collision()
        self.assertEquals(collisions, [existing_tracker_name])

    def test_code_collision_multiple_matches(self):
        signature = "toto.com"
        existing_tracker1_name = "toto"
        existing_tracker2_name = "toto"
        existing_tracker1 = Tracker(
            name=existing_tracker1_name,
            code_signature=signature,
        )
        existing_tracker1.save()
        existing_tracker2 = Tracker(
            name=existing_tracker2_name,
            code_signature=signature + '/test',
        )
        existing_tracker2.save()

        new_tracker = Tracker(
            name="toto2",
            code_signature=signature,
        )
        new_tracker.save()
        collisions = new_tracker.get_trackers_with_code_signature_collision()
        self.assertEquals(
            collisions, [existing_tracker1_name, existing_tracker2_name])

    def test_network_collision_multiple_matches(self):
        signature = "toto.com"
        existing_tracker1_name = "toto"
        existing_tracker2_name = "toto"
        existing_tracker1 = Tracker(
            name=existing_tracker1_name,
            network_signature=signature,
        )
        existing_tracker1.save()
        existing_tracker2 = Tracker(
            name=existing_tracker2_name,
            network_signature=signature + '/test',
        )
        existing_tracker2.save()

        new_tracker = Tracker(
            name="toto2",
            network_signature=signature,
        )
        new_tracker.save()
        collisions = \
            new_tracker.get_trackers_with_network_signature_collision()
        self.assertEquals(
            collisions, [existing_tracker1_name, existing_tracker2_name])

    def test_progress_empty_tracker(self):
        tracker = Tracker()
        self.assertEquals(tracker.progress(), 0)

    def test_progress_tracker_with_signatures(self):
        tracker = Tracker(
            code_signature="toto",
            network_signature="toto",
        )
        self.assertEquals(tracker.progress(), 20)

    def test_progress_tracker_with_short_signatures(self):
        tracker = Tracker(
            code_signature="tot",
            network_signature="tot",
        )
        self.assertEquals(tracker.progress(), 0)

    def test_progress_tracker_with_signatures_and_website(self):
        tracker = Tracker(
            code_signature="toto",
            network_signature="toto",
            website="toto.com",
        )
        self.assertEquals(tracker.progress(), 30)

    def test_missing_fields_empty_tracker(self):
        expected_output = [
            'Categories',
            'Description',
            'Code signature',
            'Network signature',
            'Website',
            'Capabilities',
            'Analytics',
            'Advertising',
            'Networks',
            'Maven repository',
            'Artifact ID',
            'Group ID',
            'Gradle',
        ]

        tracker = Tracker()
        self.assertEquals(tracker.missing_fields(), expected_output)

    def test_missing_fields_tracker_with_signatures(self):
        expected_output = [
            'Categories',
            'Description',
            'Website',
            'Capabilities',
            'Analytics',
            'Advertising',
            'Networks',
            'Maven repository',
            'Artifact ID',
            'Group ID',
            'Gradle',
        ]

        tracker = Tracker(
            code_signature="toto",
            network_signature="toto",
        )
        self.assertEquals(tracker.missing_fields(), expected_output)


class IndexTrackerListViewTests(TestCase):
    def test_with_trackers(self):
        tracker_1 = Tracker(
            name='name_tracker_1',
            code_signature='code_1',
            network_signature='network_1',
            website='https://website1'
        )
        tracker_2 = Tracker(
            name='random name',
            code_signature='code_2',
            network_signature='network_2',
            website='https://website2',
        )

        tracker_1.save()
        tracker_2.save()

        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tracker_1.name, 1)
        self.assertContains(response, tracker_2.name, 1)
        self.assertEqual(response.context['count'], 2)

    def test_with_search_query_with_results(self):
        tracker_1 = Tracker(
            name='match_name_tracker_1',
            code_signature='code_1',
            network_signature='network_1',
            website='https://website1'
        )
        tracker_2 = Tracker(
            name='random name',
            code_signature='tracker_code_2',
            network_signature='network_2',
            website='https://website2',
        )

        tracker_1.save()
        tracker_2.save()

        c = Client()
        response = c.get('/', {'tracker_name': 'match'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tracker_1.name, 1)
        self.assertNotContains(response, tracker_2.name)
        self.assertEqual(response.context['count'], 1)

    def test_with_only_collisions_filter(self):
        tracker_1 = Tracker(
            name='match_name_tracker_1',
            code_signature='toto.com',
            network_signature='network_1',
            website='https://website1'
        )
        tracker_2 = Tracker(
            name='random name',
            code_signature='tracker_code_2',
            network_signature='network_2',
            website='https://website2'
        )
        tracker_3 = Tracker(
            name='tracker 3',
            code_signature='toto.com',
            network_signature='network.signature',
            website='https://website3'
        )
        tracker_4 = Tracker(
            name='tracker 4',
            code_signature='code_4',
            network_signature='network.signature',
            website='https://website4'
        )

        tracker_1.save()
        tracker_2.save()
        tracker_3.save()
        tracker_4.save()

        c = Client()
        response = c.get('/', {'only_collisions': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tracker_1.name, 2)
        self.assertContains(response, tracker_3.name, 3)
        self.assertContains(response, tracker_4.name, 2)
        self.assertNotContains(response, tracker_2.name)
        self.assertEqual(response.context['count'], 3)

    def test_with_only_in_exodus_filter(self):
        tracker_not_in_exodus = Tracker.objects.create(
            name='name_tracker_1',
            code_signature='code_1',
            network_signature='network_1',
            website='https://website1'
        )
        tracker_in_exodus = Tracker.objects.create(
            name='random name',
            code_signature='code_2',
            network_signature='network_2',
            website='https://website2',
            is_in_exodus=True
        )

        c = Client()
        response = c.get('/', {'trackers_select': 'exodus'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 1)
        self.assertContains(response, tracker_in_exodus.name, 1)
        self.assertNotContains(response, tracker_not_in_exodus.name)

    def test_with_only_in_etip_filter(self):
        tracker_not_in_exodus = Tracker.objects.create(
            name='name_tracker_1',
            code_signature='code_1',
            network_signature='network_1',
            website='https://website1'
        )
        tracker_in_exodus = Tracker.objects.create(
            name='random name',
            code_signature='code_2',
            network_signature='network_2',
            website='https://website2',
            is_in_exodus=True
        )

        c = Client()
        response = c.get('/', {'trackers_select': 'etip'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 1)
        self.assertContains(response, tracker_not_in_exodus.name, 1)
        self.assertNotContains(response, tracker_in_exodus.name)

    def test_with_all_trackers_filter(self):
        tracker_not_in_exodus = Tracker.objects.create(
            name='name_tracker_1',
            code_signature='code_1',
            network_signature='network_1',
            website='https://website1'
        )
        tracker_in_exodus = Tracker.objects.create(
            name='random name',
            code_signature='code_2',
            network_signature='network_2',
            website='https://website2',
            is_in_exodus=True
        )

        c = Client()
        response = c.get('/', {'trackers_select': 'all'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['count'], 2)
        self.assertContains(response, tracker_not_in_exodus.name, 1)
        self.assertContains(response, tracker_in_exodus.name, 1)

    def test_with_only_collisions_filter_without_collisions(self):
        tracker_1 = Tracker(
            name='match_name_tracker_1',
            code_signature='toto.com',
            network_signature='network_1',
            website='https://website1'
        )
        tracker_2 = Tracker(
            name='random name',
            code_signature='tracker_code_2',
            network_signature='network_2',
            website='https://website2',
        )

        tracker_1.save()
        tracker_2.save()

        c = Client()
        response = c.get('/', {'only_collisions': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, tracker_1.name)
        self.assertNotContains(response, tracker_2.name)
        self.assertEqual(response.context['count'], 0)

    def test_with_results_and_paginate(self):
        for i in range(0, 25):
            Tracker(
                name='AcTracker_name'
            ).save()

        for i in range(0, 10):
            Tracker(
                name='AbTracker_name'
            ).save()

        c = Client()
        response = c.get(
            '/',
            {'tracker_name': 'Ac', 'page': 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Ab')
        self.assertEqual(response.context['count'], 25)
        self.assertEqual(len(response.context['trackers']), 5)

    def test_with_all_filters_and_paginate(self):
        for i in range(0, 25):
            Tracker(
                name='AcTracker_name',
                code_signature='toto.com'
            ).save()

        for i in range(0, 10):
            Tracker(
                name='AbTracker_name'
            ).save()

        c = Client()
        response = c.get(
            '/',
            {'tracker_name': 'Ac', 'only_collisions': 'true', 'page': 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Ab')
        self.assertEqual(response.context['count'], 25)
        self.assertEqual(len(response.context['trackers']), 5)


class DisplayTrackerListViewTests(TestCase):
    def test_returns_404_if_missing_tracker(self):
        c = Client()
        response = c.get('/trackers/00b4c3a3-7240-4ffa-8525-3bc934157ccf/')
        self.assertEqual(response.status_code, 404)

    def test_returns_404_if_wrong_uid(self):
        c = Client()
        response = c.get('/trackers/1/')
        self.assertEqual(response.status_code, 404)

    def test_returns_something_where_valid_tracker(self):
        tracker = Tracker.objects.create(
            name='name_tracker_1',
            code_signature='code_1',
            network_signature='network_1',
            website='https://website1'
        )

        c = Client()
        response = c.get('/trackers/{}/'.format(tracker.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tracker.name, 1)
        self.assertNotContains(response, "Collision detected")

    def test_displays_collision_when_code_collision(self):
        tracker_1 = Tracker.objects.create(
            name='match_name_tracker_1',
            code_signature='toto.com',
            network_signature='network_1',
            website='https://website1'
        )
        tracker_2 = Tracker.objects.create(
            name='tracker 2',
            code_signature='toto.com',
            network_signature='network.signature',
            website='https://website2'
        )
        expected_message = "{} (code signature)".format(tracker_2.name)

        c = Client()
        response = c.get('/trackers/{}/'.format(tracker_1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Collision detected")
        self.assertContains(response, expected_message)

    def test_displays_collision_when_network_collision(self):
        tracker_1 = Tracker.objects.create(
            name='tracker 1',
            code_signature='toto.com',
            network_signature='network.signature',
            website='https://website1'
        )
        tracker_2 = Tracker.objects.create(
            name='tracker 2',
            code_signature='code_2',
            network_signature='network.signature',
            website='https://website2'
        )
        expected_message = "{} (network signature)".format(tracker_2.name)

        c = Client()
        response = c.get('/trackers/{}/'.format(tracker_1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Collision detected")
        self.assertContains(response, expected_message)


class ExportTrackerListViewTests(TestCase):
    def test_without_trackers(self):
        c = Client()
        response = c.get('/trackers/export')
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode('utf-8'), {'trackers': []})

    def test_with_trackers(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            network_signature='network_1',
            website='https://website1'
        )

        tracker_2 = Tracker(
            name='tracker_2',
            code_signature='code_2',
            network_signature='network_2',
            website='https://website2',
            description='description du tracker_2'
        )

        tracker_1.save()
        tracker_2.save()

        c = Client()
        response = c.get('/trackers/export')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.get('Content-Disposition'),
                          'attachment; filename=trackers.json')
        f = BytesIO(response.content)
        expected_json = {
            'trackers': [
                {
                    'name': tracker_1.name,
                    'code_signature': tracker_1.code_signature,
                    'network_signature': tracker_1.network_signature,
                    'website': tracker_1.website
                },
                {
                    'name': tracker_2.name,
                    'code_signature': tracker_2.code_signature,
                    'network_signature': tracker_2.network_signature,
                    'website': tracker_2.website
                }
            ]
        }
        self.assertJSONEqual(f.getvalue().decode('utf-8'), expected_json)


class CompareTrackersWithExodusCommandTest(TestCase):

    EXODUS_API_BASE_URL = 'https://reports.exodus-privacy.eu.org'
    EXODUS_API_BASE_PATH = '/api/trackers'

    def test_api_gets_called_correctly(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            call_command('compare_with_exodus', stdout=StringIO())
        mocked_get.assert_called_with(
            self.EXODUS_API_BASE_URL + self.EXODUS_API_BASE_PATH
        )

    def test_api_gets_called_with_provided_url(self):
        fake_url = 'https://example.com'
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            call_command(
                'compare_with_exodus', stdout=StringIO(),
                exodus_hostname=fake_url
            )
        mocked_get.assert_called_with(fake_url + self.EXODUS_API_BASE_PATH)

    def test_raise_error_when_api_not_200(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 404
            with self.assertRaises(CommandError) as e:
                call_command('compare_with_exodus', stdout=StringIO())
        error_msg = str(e.exception)
        self.assertEqual(error_msg, 'Unexpected status from API: 404')

    def test_raise_error_when_empty_response(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json.return_value = {}
            with self.assertRaises(CommandError) as e:
                call_command('compare_with_exodus', stdout=StringIO())
        error_msg = str(e.exception)
        self.assertEqual(error_msg, 'Empty response')

    def test_select_only_in_exodus_trackers(self):
        Tracker(name="In Exodus", is_in_exodus=True).save()
        Tracker(name="Not In Exodus", is_in_exodus=False).save()
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            out = StringIO()
            call_command('compare_with_exodus', stdout=out)
        self.assertIn('Found 1 trackers in ETIP DB', out.getvalue())

    def __build_json_mock_response(self, trackers_list):
        mocked_json = {'trackers': {}}
        for idx, tracker in enumerate(trackers_list):
            mocked_json['trackers'][idx + 1] = {
                'name': tracker.name,
                'code_signature': tracker.code_signature,
                'description': tracker.description,
                'network_signature': tracker.network_signature,
                'website': tracker.website
            }
        return mocked_json

    def __call_command(self, status_code, mocked_json, options):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = status_code
            mocked_get.return_value.json.return_value = mocked_json
            out = StringIO()
            call_command('compare_with_exodus', stdout=out, *options)
        return out

    def test_find_1_exact_match(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            description='description 1',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_1.save()
        mocked_json = self.__build_json_mock_response([tracker_1])
        expected_answer = (
            "Retrieved 1 trackers from Exodus\n"
            "Found 1 trackers in ETIP DB expected to be in Exodus\n"
            "Starting case-sensitive lookup...\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 1\n"
            "** FOUND_BUT_DIFFERENT: 0\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 0\n"
            "** NOT_FOUND_IN_ETIP: 0\n"
        )
        out = self.__call_command(200, mocked_json, [])
        self.assertIn(expected_answer, out.getvalue())

    def test_find_1_exact_match_and_1_not_found(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            description='description 1',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_2 = Tracker(
            name='tracker_2',
            code_signature='code_2',
            description='description 2',
            network_signature='network_2',
            website='https://website2',
            is_in_exodus=True
        )
        tracker_1.save()
        mocked_json = self.__build_json_mock_response([tracker_1, tracker_2])
        expected_answer = (
            "Retrieved 2 trackers from Exodus\n"
            "Found 1 trackers in ETIP DB expected to be in Exodus\n"
            "Starting case-sensitive lookup...\n"
            "NOT_FOUND_IN_ETIP - tracker_2\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 1\n"
            "** FOUND_BUT_DIFFERENT: 0\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 0\n"
            "** NOT_FOUND_IN_ETIP: 1\n"
        )

        out = self.__call_command(200, mocked_json, [])
        self.assertIn(expected_answer, out.getvalue())

    def test_find_1_different(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            description='description 1',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_1.save()
        mocked_json = self.__build_json_mock_response([tracker_1])
        mocked_json['trackers'][1]['code_signature'] = 'another_signature'
        expected_answer = (
            "Retrieved 1 trackers from Exodus\n"
            "Found 1 trackers in ETIP DB expected to be in Exodus\n"
            "Starting case-sensitive lookup...\n"
            "FOUND_BUT_DIFFERENT - tracker_1\n"
            "[code_signature]\n"
            "etip  : code_1\n"
            "exodus: another_signature\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 0\n"
            "** FOUND_BUT_DIFFERENT: 1\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 0\n"
            "** NOT_FOUND_IN_ETIP: 0\n"
        )
        out = self.__call_command(200, mocked_json, [])
        self.assertIn(expected_answer, out.getvalue())

    def test_find_multiple_same_name(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            description='description 1',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_2 = Tracker(
            name='tracker_1',
            code_signature='code_2',
            description='description 2',
            network_signature='network_2',
            website='https://website2',
            is_in_exodus=True
        )
        tracker_1.save()
        tracker_2.save()
        mocked_json = self.__build_json_mock_response([tracker_1])
        expected_answer = (
            "Retrieved 1 trackers from Exodus\n"
            "Found 2 trackers in ETIP DB expected to be in Exodus\n"
            "Starting case-sensitive lookup...\n"
            "MULTIPLE_MATCHES_FOUND_IN_ETIP - tracker_1\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 0\n"
            "** FOUND_BUT_DIFFERENT: 0\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 1\n"
            "** NOT_FOUND_IN_ETIP: 0\n"
        )
        out = self.__call_command(200, mocked_json, [])
        self.assertIn(expected_answer, out.getvalue())

    def test_find_multiple_same_code_signature(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            description='description 1',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_2 = Tracker(
            name='tracker_2',
            code_signature='code_1',
            description='description 2',
            network_signature='network_2',
            website='https://website2',
            is_in_exodus=True
        )
        tracker_1.save()
        tracker_2.save()
        mocked_json = self.__build_json_mock_response([tracker_1])
        expected_answer = (
            "Retrieved 1 trackers from Exodus\n"
            "Found 2 trackers in ETIP DB expected to be in Exodus\n"
            "Starting case-sensitive lookup...\n"
            "MULTIPLE_MATCHES_FOUND_IN_ETIP - tracker_1\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 0\n"
            "** FOUND_BUT_DIFFERENT: 0\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 1\n"
            "** NOT_FOUND_IN_ETIP: 0\n"
        )
        out = self.__call_command(200, mocked_json, [])
        self.assertIn(expected_answer, out.getvalue())

    def test_find_one_of_each(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            description='description 1',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_2 = Tracker(
            name='tracker_2',
            code_signature='code_2',
            description='description 2',
            network_signature='network_2',
            website='https://website2',
            is_in_exodus=True
        )
        tracker_3 = Tracker(
            name='tracker_3',
            code_signature='code_3',
            description='description 3',
            network_signature='network_3',
            website='https://website3',
            is_in_exodus=True
        )
        tracker_3bis = Tracker(
            name='tracker_3',
            code_signature='code_3',
            description='description 3',
            network_signature='network_3',
            website='https://website3',
            is_in_exodus=True
        )
        tracker_4 = Tracker(
            name='tracker_4',
            code_signature='code_4',
            description='description 4',
            network_signature='network_4',
            website='https://website4',
            is_in_exodus=True
        )
        tracker_1.save()
        tracker_2.save()
        tracker_3.save()
        tracker_3bis.save()
        mocked_json = self.__build_json_mock_response([
            tracker_1, tracker_2, tracker_3, tracker_4
        ])
        mocked_json['trackers'][2]['website'] = 'another_website'
        expected_answer = (
            "Retrieved 4 trackers from Exodus\n"
            "Found 4 trackers in ETIP DB expected to be in Exodus\n"
            "Starting case-sensitive lookup...\n"
            "FOUND_BUT_DIFFERENT - tracker_2\n"
            "[website]\n"
            "etip  : https://website2\n"
            "exodus: another_website\n"
            "MULTIPLE_MATCHES_FOUND_IN_ETIP - tracker_3\n"
            "NOT_FOUND_IN_ETIP - tracker_4\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 1\n"
            "** FOUND_BUT_DIFFERENT: 1\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 1\n"
            "** NOT_FOUND_IN_ETIP: 1\n"
        )
        out = self.__call_command(200, mocked_json, [])
        self.assertIn(expected_answer, out.getvalue())

    def test_1_different_in_quiet_mode(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            description='description 1',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_1.save()
        mocked_json = self.__build_json_mock_response([tracker_1])
        mocked_json['trackers'][1]['code_signature'] = 'another_signature'
        expected_answer = (
            "Retrieved 1 trackers from Exodus\n"
            "Found 1 trackers in ETIP DB expected to be in Exodus\n"
            "Using quiet mode; Not going to display diff details.\n"
            "Starting case-sensitive lookup...\n"
            "FOUND_BUT_DIFFERENT - tracker_1\n"
            "[code_signature]\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 0\n"
            "** FOUND_BUT_DIFFERENT: 1\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 0\n"
            "** NOT_FOUND_IN_ETIP: 0\n"
        )
        out = self.__call_command(200, mocked_json, ['-q'])
        self.assertIn(expected_answer, out.getvalue())

    def test_consider_identical_because_ignore_one_field(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_1.save()
        mocked_json = self.__build_json_mock_response([tracker_1])
        mocked_json['trackers'][1]['code_signature'] = 'another_signature'
        expected_answer = (
            "Retrieved 1 trackers from Exodus\n"
            "Found 1 trackers in ETIP DB expected to be in Exodus\n"
            "Going to ignore field code_signature in comparison.\n"
            "Starting case-sensitive lookup...\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 1\n"
            "** FOUND_BUT_DIFFERENT: 0\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 0\n"
            "** NOT_FOUND_IN_ETIP: 0\n"
        )
        out = self.__call_command(
            200, mocked_json, ['--ignore-field', 'code_signature'])
        self.assertIn(expected_answer, out.getvalue())

    def test_different_description(self):
        tracker_1 = Tracker(
            name='tracker_1',
            code_signature='code_1',
            description='my simple description',
            network_signature='network_1',
            website='https://website1',
            is_in_exodus=True
        )
        tracker_1.save()
        mocked_json = self.__build_json_mock_response([tracker_1])
        mocked_json['trackers'][1]['description'] = 'another description'
        expected_answer = (
            "Retrieved 1 trackers from Exodus\n"
            "Found 1 trackers in ETIP DB expected to be in Exodus\n"
            "Starting case-sensitive lookup...\n"
            "FOUND_BUT_DIFFERENT - tracker_1\n"
            "[description]\n"
            "etip  : my simple description\n"
            "exodus: another description\n"
            "Lookup results:\n"
            "** FOUND_AND_IDENTICAL: 0\n"
            "** FOUND_BUT_DIFFERENT: 1\n"
            "** MULTIPLE_MATCHES_FOUND_IN_ETIP: 0\n"
            "** NOT_FOUND_IN_ETIP: 0\n"
        )
        out = self.__call_command(200, mocked_json, [])
        self.assertIn(expected_answer, out.getvalue())


class ImportCategoriesCommandTest(TestCase):

    CMD_NAME = 'import_categories'

    def test_logs_are_printed(self):
        expected_output = (
            "Capability categories created\n"
            "Advertising categories created\n"
            "Analytic categories created\n"
            "Network categories created\n"
            "Tracker categories created\n"
        )

        out = StringIO()
        call_command(self.CMD_NAME, stdout=out)
        self.assertIn(expected_output, out.getvalue())

    def test_categories_are_created(self):
        out = StringIO()
        call_command(self.CMD_NAME, stdout=out)

        self.assertEquals(Capability.objects.all().count(), 8)
        self.assertEquals(Advertising.objects.all().count(), 9)
        self.assertEquals(Analytic.objects.all().count(), 14)
        self.assertEquals(Network.objects.all().count(), 9)
        self.assertEquals(TrackerCategory.objects.all().count(), 6)

    def test_categories_are_created_only_once(self):
        out = StringIO()
        call_command(self.CMD_NAME, stdout=out)
        call_command(self.CMD_NAME, stdout=out)

        self.assertEquals(Capability.objects.all().count(), 8)
        self.assertEquals(Advertising.objects.all().count(), 9)
        self.assertEquals(Analytic.objects.all().count(), 14)
        self.assertEquals(Network.objects.all().count(), 9)
        self.assertEquals(TrackerCategory.objects.all().count(), 6)
