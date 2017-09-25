import unittest
from dictogram import Dictogram


class TestDictogram(unittest.TestCase):
    words = ('a', 'b', 'c',)

    def test_init_1(self):
        dsg = Dictogram()
        self.assertEquals({}, dsg)

    def test_init_2(self):
        dsg = Dictogram(self.words)
        self.assertEquals({'a': 1, 'b': 1, 'c': 1}, dsg)

    def test_update_1(self):
        dsg = Dictogram()
        dsg.update(self.words)
        self.assertEquals({'a': 1, 'b': 1, 'c': 1}, dsg)

    def test_update_2(self):
        dsg = Dictogram(self.words)
        dsg.update(self.words)
        self.assertEquals({'a': 2, 'b': 2, 'c': 2}, dsg)
        dsg.update(('c', 'b',))
        self.assertEquals({'a': 2, 'b': 3, 'c': 3}, dsg)
        dsg.update(('b',))
        self.assertEquals({'a': 2, 'b': 4, 'c': 3}, dsg)

    def test_get_random_weighted_item(self):
        dsg = Dictogram(self.words)
        dsg.update(('c',))
        random_item = dsg._get_random_item_by_weight(2)
        self.assertEqual(random_item[0], 'c')
        dsg.update(('b',))
        dsg.update(('c',))
        random_item = dsg._get_random_item_by_weight(3)
        self.assertEqual(random_item[0], 'c')

    def test_get_random_word(self):
        dsg = Dictogram(self.words)
        random_word = dsg.get_weighted_random_word()
        self.assertTrue(random_word in self.words)
