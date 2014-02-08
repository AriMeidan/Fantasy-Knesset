# coding=utf-8

'''
Copyright 2014 Ari Meidan and Tom Gurion

This file is part of "Games of Knesset".

"Games of Knesset" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"Games of Knesset" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with "Games of Knesset".  If not, see <http://www.gnu.org/licenses/>.
'''



import os
import csv

from django.core.management.base import BaseCommand, CommandError

from fknesset.settings.base import BASE_DIR
from votes.models import Party, Candidate


class Command(BaseCommand):
    help = 'Run it to fill the DB with candidates and parties' \
           'from "19th knesset.csv"'

    def handle(self, *args, **options):
        path = os.path.join(BASE_DIR,
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

        # adding independent party to the DB
        Party.objects.get_or_create(name=u'לא משוייך')
