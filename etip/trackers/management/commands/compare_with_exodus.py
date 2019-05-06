from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from functools import reduce
import operator
import requests

from trackers.models import Tracker

EXODUS_API_DEFAULT_HOSTNAME = 'https://reports.exodus-privacy.eu.org'
EXODUS_API_PATH = '/api/trackers'
FIELDS_TO_SEARCH = [
    'name',
    'code_signature'
]
FIELDS_TO_COMPARE = [
    'name',
    'code_signature',
    'network_signature',
    'website'
]
FOUND_AND_IDENTICAL = 'FOUND_AND_IDENTICAL'
FOUND_BUT_DIFFERENT = 'FOUND_BUT_DIFFERENT'
MULTIPLE_FOUND = 'MULTIPLE_MATCHES_FOUND_IN_ETIP'
NOT_FOUND = 'NOT_FOUND_IN_ETIP'
TYPES = [FOUND_AND_IDENTICAL, FOUND_BUT_DIFFERENT, MULTIPLE_FOUND, NOT_FOUND]


class Command(BaseCommand):
    help = 'Compare trackers stored in Exodus with trackers from ETIP DB'

    def add_arguments(self, parser):
        parser.add_argument(
            '-e',
            '--exodus-hostname',
            type=str,
            nargs='?',
            default=EXODUS_API_DEFAULT_HOSTNAME,
            help='Specify the Hostname of the Exodus instance to query.' +
            ' Default is public instance of Exodus reports.',
        )
        parser.add_argument(
            '-q',
            '--quiet',
            action='store_true',
            default=False,
            help='Hide details of differences when tracker is ' +
            'found but different'
        )

    def handle(self, *args, **options):
        exodus_trackers = self.get_all_from_exodus(options['exodus_hostname'])
        self.stdout.write(
            'Retrieved {} trackers from Exodus'.format(len(exodus_trackers))
        )
        self.count_etip_trackers()
        self.lookup_trackers(exodus_trackers, options['quiet'])

    def get_diff_fields(self, exodus_tracker, etip_tracker):
        diff_fields = []
        for field in FIELDS_TO_COMPARE:
            if getattr(etip_tracker, field) != exodus_tracker.get(field):
                diff_fields.append(field)
        return diff_fields

    def build_query(self, tracker_details):
        filters = []
        for field in FIELDS_TO_SEARCH:
            args = {field + '__exact': tracker_details.get(field)}
            filters.append(Q(**args))
        return reduce(operator.or_, filters)

    def display_diff(self, diff_fields, exodus_tracker, etip_tracker):
        for field in diff_fields:
            self.stdout.write('[{}]'.format(field))
            self.stdout.write('etip  : {}'.format(
                getattr(etip_tracker, field)
            ))
            self.stdout.write('exodus: {}'.format(
                exodus_tracker.get(field)
            ))

    def find_etip_tracker(self, tracker_details, is_quiet):
        search_filters = self.build_query(tracker_details)
        try:
            etip_tracker = Tracker.objects.exclude(
                is_in_exodus=False
            ).get(search_filters)
        except MultipleObjectsReturned:
            if not is_quiet:
                self.stdout.write('{} - {}'.format(
                    MULTIPLE_FOUND, tracker_details.get('name'))
                )
            return MULTIPLE_FOUND
        except ObjectDoesNotExist:
            if not is_quiet:
                self.stdout.write('{} - {}'.format(
                    NOT_FOUND, tracker_details.get('name'))
                )
            return NOT_FOUND
        diff_fields = self.get_diff_fields(tracker_details, etip_tracker)
        if (len(diff_fields) == 0):
            return FOUND_AND_IDENTICAL
        else:
            if not is_quiet:
                self.stdout.write('{} - {}'.format(
                    FOUND_BUT_DIFFERENT, tracker_details.get('name'))
                )
                self.display_diff(diff_fields, tracker_details, etip_tracker)
            return FOUND_BUT_DIFFERENT

    def lookup_trackers(self, exodus_trackers, is_quiet):
        result_counters = {t: 0 for t in TYPES}

        self.stdout.write('Starting case-sensitive lookup...')
        for id, tracker_details in exodus_trackers.items():
            lookup_result = self.find_etip_tracker(tracker_details, is_quiet)
            result_counters[lookup_result] += 1
        self.stdout.write('Lookup results:')
        for type in TYPES:
            self.stdout.write('** {}: {}'.format(type, result_counters[type]))

    def get_all_from_exodus(self, exodus_base_url):
        response = requests.get(exodus_base_url + EXODUS_API_PATH)
        if response.status_code != 200:
            raise CommandError(
                'Unexpected status from API: {}'
                .format(response.status_code)
            )
        resp = response.json()
        if resp is None or resp.get('trackers') is None:
            raise CommandError('Empty response')
        return resp.get('trackers')

    def count_etip_trackers(self):
        nb_of_trackers = Tracker.objects.filter(is_in_exodus=True).count()
        self.stdout.write(
            'Found {} trackers in ETIP DB expected to be in Exodus'.format(
                nb_of_trackers
            )
        )
