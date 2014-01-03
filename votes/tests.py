# coding=utf-8

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
