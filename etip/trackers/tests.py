from django.test import TestCase, Client
from .models import Tracker
from io import BytesIO


class TrackerModelTests(TestCase):

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
        collisions = new_tracker.code_signature_collision()
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
        collisions = new_tracker.code_signature_collision()
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
        collisions = new_tracker.network_signature_collision()
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
        collisions = new_tracker.network_signature_collision()
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
        collisions = new_tracker.code_signature_collision()
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
        collisions = new_tracker.code_signature_collision()
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
        collisions = new_tracker.network_signature_collision()
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
            'Long description',
            'Short description',
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
            'Long description',
            'Short description',
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
        response = c.get('/', {'tracker_name': 'Ac', 'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Ab')
        self.assertEqual(response.context['count'], 25)
        self.assertEqual(len(response.context['trackers']), 5)


class ExportTrackerListViewTests(TestCase):
    def test_without_trackers(self):
        c = Client()
        response = c.get('/trackers/export')
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content, {'trackers': []})

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
        self.assertJSONEqual(f.getvalue(), expected_json)
