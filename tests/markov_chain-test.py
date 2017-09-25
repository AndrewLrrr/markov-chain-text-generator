import unittest

from markov_chain import MarkovChain


class TestMarkovChain(unittest.TestCase):
    def test_add_N_1(self):
        mc = MarkovChain()
        mc.add(('a', 'b', 'c',))
        self.assertEqual({
            ('a',): {'b': 1},
            ('b',): {'c': 1},
            'START': {('a',): 1},
        }, mc.model)

        mc.add(('b', 'a',))
        self.assertEqual({
            ('a',): {'b': 1},
            ('b',): {'c': 1, 'a': 1},
            'START': {('a',): 1, ('b',): 1},
        }, mc.model)

        mc.add(('a', 'c',))
        self.assertEqual({
            ('a',): {'b': 1, 'c': 1},
            ('b',): {'c': 1, 'a': 1},
            'START': {('a',): 2, ('b',): 1},
        }, mc.model)

    def test_add_N_2(self):
        mc = MarkovChain(2)
        mc.add(('a', 'b', 'c', 'd', 'a', 'b', 'e',))
        self.assertEqual({
            ('a', 'b',): {'c': 1, 'e': 1},
            ('b', 'c',): {'d': 1},
            ('c', 'd',): {'a': 1},
            ('d', 'a',): {'b': 1},
            'START': {('a', 'b'): 1},
        }, mc.model)

        mc.add(('a', 'b', 'e', 'd',))
        self.assertEqual({
            ('a', 'b',): {'c': 1, 'e': 2},
            ('b', 'c',): {'d': 1},
            ('c', 'd',): {'a': 1},
            ('d', 'a',): {'b': 1},
            ('b', 'e'): {'d': 1},
            'START': {('a', 'b'): 2},
        }, mc.model)

    def test_parse_and_add(self):
        mc = MarkovChain()
        mc.parse_and_add('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ornare placerat fringilla.')
        self.assertEqual({
            ('Lorem',): {'ipsum': 1},
            ('ipsum',): {'dolor': 1},
            ('dolor',): {'sit': 1},
            ('sit',): {'amet,': 1},
            ('amet,',): {'consectetur': 1},
            ('consectetur',): {'adipiscing': 1},
            ('adipiscing',): {'elit.': 1},
            ('Donec',): {'ornare': 1},
            ('ornare',): {'placerat': 1},
            ('placerat',): {'fringilla.': 1},
            'START': {('Lorem',): 1, ('Donec',): 1},
        }, mc.model)

    def test_generate_sentence(self):
        mc = MarkovChain()
        mc.add(('aaa', 'bbb.', 'ccc'))
        self.assertEqual('Aaa bbb.', mc.generate_sentence(12))
        self.assertEqual('Aaa bbb. Ccc.', mc.generate_sentence(13))
