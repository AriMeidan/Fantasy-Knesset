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

from django.test import TestCase

from models import Party, Candidate

# Create your tests here.
class PartyModelTests(TestCase):

    def test_unicode(self):
        p = Party.objects.create(name='Avoda')
        self.assertEqual(str(p), 'Avoda')
        p = Party.objects.create(name=u'עבודה')
        self.assertEqual(str(p).decode('utf-8'), u'עבודה')


class CandidateModelTests(TestCase):

    def test_unicode(self):
        c = Candidate.objects.create(name='Ahmad Tibi')
        self.assertEqual(str(c), 'Ahmad Tibi')
        c = Candidate.objects.create(name=u'אחמד טיבי')
        self.assertEqual(str(c).decode('utf-8'), u'אחמד טיבי')

    def test_ordering(self):
        c1 = Candidate.objects.create(name='C1', number_of_votes=8)
        c2 = Candidate.objects.create(name='C2', number_of_votes=14)
        c3 = Candidate.objects.create(name='C3', number_of_votes=4)
        c4 = Candidate.objects.create(name='C4', number_of_votes=11)
        c5 = Candidate.objects.create(name='C5', number_of_votes=13)
        self.assertQuerysetEqual(Candidate.objects.all(),
                                 [c2, c5, c4, c1, c3],
                                 transform=lambda x: x)
