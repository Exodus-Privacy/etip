import json

from django.core.management.base import BaseCommand, CommandError

from trackers.models import Tracker


def read_file(filename):
    if filename.find('://') > 0:
        import urllib.request

        file = urllib.request.urlopen(filename)
    else:
        file = open(filename, 'r')

    return file.read()


class Command(BaseCommand):
    help = 'Import trackers from exodus'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs='?',
            default='https://reports.exodus-privacy.eu.org/api/trackers'
        )

    def handle(self, *args, **options):
        if Tracker.objects.all().count() > 0:
            raise CommandError('Your trackers table in not empty, '
                               'please truncate it before the import')

        json_str = read_file(options['filename']).decode('utf-8')
        trackers = json.loads(json_str)

        for _, tracker in trackers['trackers'].items():
            model = Tracker(
                name=tracker['name'],
                description=tracker['description'],
                created=tracker['creation_date'],
                code_signature=tracker['code_signature'],
                network_signature=tracker['network_signature'],
                website=tracker['website'],
                is_in_exodus=True,
            )

            model.save()

            print('%s saved' % model.name)
