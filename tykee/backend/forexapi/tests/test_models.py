from django.test import TestCase

from forexapi.models import Strategies


class TestModels(TestCase):
    def test_find_by_name(self):
        strategy = Strategies.objects.get(name='test')
        self.assertEqual(strategy.name, 'test')
        self.assertEqual(strategy.strategy_id, 1)
