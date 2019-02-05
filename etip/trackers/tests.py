from django.test import TestCase
from .models import Tracker


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
