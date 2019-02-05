from django.core.management.base import BaseCommand

from trackers.models import Capability, Advertising, Analytic, Network


class Command(BaseCommand):
    help = 'Import trackers categories'

    def handle(self, *args, **options):
        capability_names = [
            'Tracks users using bluetooth',
            'Tracks users using ultrasonic',
            'Tracks users using location data',
            'Tracks users using GPS',
            'Tracks users using WiFi',
            'Tracks users using NFC',
            'Targets user location and proximity via geofencing',
            'Targets users via geotargeting',
        ]

        for name in capability_names:
            m = Capability(name=name)
            m.save()

        advertising_names = [
            'Loads advertisements',
            'Loads targeted advertisements',
            'Real-world location targeting',
            'Targeted advertising based on consumer actions',
            'Timed advertisements',
            'Targets across devices, channels and/or platforms (omni-channel marketing, customer journey)',
            'Bidding services',
            'Location-based ad pushing',
            'Alters app functionality based upon user profiles',
        ]

        for name in advertising_names:
            m = Advertising(name=name)
            m.save()

        analytic_names = [
            'Offers analytics activity to app developers',
            'Offers reports to app developers',
            'Collects Personally Identifiable Information (PII)',
            'Collects Sensitive Personal Information (SPI)',
            'Profiles users via Personally Identifiable Information (PII)',
            'Profiles users via Sensitive Personal Information (SPI)',
            'Performs cross-device identification',
            'Identifies users via Google ID (AAID)',
            'Identifies users via iOS ID (IDFA)',
            'Identifies users via network ID (hostname/ISP/SSID)',
            'Stores facial recognition data',
            'Stores personal profile data (name, address, phone)',
            'Analytics AI and machine learning',
            'Audience segmenting',
        ]

        for name in analytic_names:
            m = Analytic(name=name)
            m.save()

        network_names = [
            'Transmits user data to multiple ad networks',
            'Transmits information to Facebook ad network',
            'Transmits information to Google ad network',
            'Transmits information to Adobe ad network',
            'Transmits information to Yahoo! ad network',
            'Transmits information to Salesforce platform',
            'Transmits information to Twitter platform',
            'Transmits information to Amazon ad network',
            'Transmits information to Microsoft ad network',
        ]

        for name in network_names:
            m = Network(name=name)
            m.save()
