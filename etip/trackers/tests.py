from django.test import TestCase
from .models import Tracker


class TrackerModelTests(TestCase):

    def test_code_collision_different_signature(self):
        existing_tracker = Tracker(
            name="toto",
            code_signature="toto.com",
        )
        existing_tracker.save()

        new_tracker = Tracker()
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
        collisions = new_tracker.network_signature_collision()
        self.assertEquals(collisions, [existing_tracker_name])

    def test_network_collision_contains_signature(self):
        existing_tracker_name = "toto"
        signature = "toto.com"
        existing_tracker = Tracker(
            name=existing_tracker_name,
            network_signature=signature+'/test',
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="toto2",
            network_signature=signature,
        )
        collisions = new_tracker.network_signature_collision()
        self.assertEquals(collisions, [existing_tracker_name])

    def test_code_collision_contains_signature(self):
        existing_tracker_name = "toto"
        signature = "toto.com"
        existing_tracker = Tracker(
            name=existing_tracker_name,
            code_signature=signature+'/test',
        )
        existing_tracker.save()

        new_tracker = Tracker(
            name="toto2",
            code_signature=signature,
        )
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
            code_signature=signature+'/test',
        )
        existing_tracker2.save()

        new_tracker = Tracker(
            name="toto2",
            code_signature=signature,
        )
        collisions = new_tracker.code_signature_collision()
        self.assertEquals(collisions, [existing_tracker1_name, existing_tracker2_name])

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
            network_signature=signature+'/test',
        )
        existing_tracker2.save()

        new_tracker = Tracker(
            name="toto2",
            network_signature=signature,
        )
        collisions = new_tracker.network_signature_collision()
        self.assertEquals(collisions, [existing_tracker1_name, existing_tracker2_name])
