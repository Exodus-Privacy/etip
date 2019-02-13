from django.core.management.base import BaseCommand

from trackers.models import Capability, Advertising, Analytic, Network


class Command(BaseCommand):
    help = 'Import trackers categories'

    def handle(self, *args, **options):
        m = Capability(name='Tracks users using bluetooth')
        m.save()
        m = Capability(name='Tracks users using ultrasonic')
        m.save()
        m = Capability(name='Tracks users using location data')
        m.save()
        m = Capability(name='Tracks users using GPS')
        m.save()
        m = Capability(name='Tracks users using WiFi')
        m.save()
        m = Capability(name='Tracks users using NFC')
        m.save()
        m = Capability(
            name='Targets user location and proximity via geofencing')
        m.save()
        m = Capability(name='Targets users via geotargeting')
        m.save()

        m = Advertising(name='Loads advertisements')
        m.save()
        m = Advertising(name='Loads targeted advertisements')
        m.save()
        m = Advertising(name='Real-world location targeting')
        m.save()
        m = Advertising(name='Targeted advertising based on consumer actions')
        m.save()
        m = Advertising(name='Timed advertisements')
        m.save()
        m = Advertising(
            name='Targets across devices, channels and/or platforms \
            (omni-channel marketing, customer journey)')
        m.save()
        m = Advertising(name='Bidding services')
        m.save()
        m = Advertising(name='Location-based ad pushing')
        m.save()
        m = Advertising(
            name='Alters app functionality based upon user profiles')
        m.save()

        m = Analytic(name='Offers analytics activity to app developers')
        m.save()
        m = Analytic(name='Offers reports to app developers')
        m.save()
        m = Analytic(name='Collects Personally Identifiable Information (PII)')
        m.save()
        m = Analytic(name='Collects Sensitive Personal Information (SPI)')
        m.save()
        m = Analytic(
            name='Profiles users via Personally Identifiable Information \
            (PII)')
        m.save()
        m = Analytic(
            name='Profiles users via Sensitive Personal Information (SPI)')
        m.save()
        m = Analytic(name='Performs cross-device identification')
        m.save()
        m = Analytic(name='Identifies users via Google ID (AAID)')
        m.save()
        m = Analytic(name='Identifies users via iOS ID (IDFA)')
        m.save()
        m = Analytic(
            name='Identifies users via network ID (hostname/ISP/SSID)')
        m.save()
        m = Analytic(name='Stores facial recognition data')
        m.save()
        m = Analytic(
            name='Stores personal profile data (name, address, phone)')
        m.save()
        m = Analytic(name='Analytics AI and machine learning')
        m.save()
        m = Analytic(name='Audience segmenting')
        m.save()

        m = Network(name='Transmits user data to multiple ad networks')
        m.save()
        m = Network(name='Transmits information to Facebook ad network')
        m.save()
        m = Network(name='Transmits information to Google ad network')
        m.save()
        m = Network(name='Transmits information to Adobe ad network')
        m.save()
        m = Network(name='Transmits information to Yahoo! ad network')
        m.save()
        m = Network(name='Transmits information to Salesforce platform')
        m.save()
        m = Network(name='Transmits information to Twitter platform')
        m.save()
        m = Network(name='Transmits information to Amazon ad network')
        m.save()
        m = Network(name='Transmits information to Microsoft ad network')
        m.save()
