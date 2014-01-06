import os
import csv

from django.core.management.base import BaseCommand, CommandError

from fknesset import settings
from votes.models import Party, Candidate


class Command(BaseCommand):
    help = 'Run it to fill the DB with candidates and parties' \
           'from "19th knesset.csv"'

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR,
                            'docs',
                            '19th_knesset.csv')
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if reader.line_num != 1:  # skip first row
                    p, created = Party.objects.get_or_create(
                        name=row[2])
                    c = Candidate.objects.get_or_create(
                        name=row[1], party=p, is_knesset_member=True,
                        image_url=row[4]
                    )
