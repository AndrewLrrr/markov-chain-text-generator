import random


class Dictogram(dict):
    def __init__(self, iterable=None):
        super(Dictogram, self).__init__()
        if iterable:
            self.update(iterable)

    def update(self, iterable, **kwargs):
        for i in iterable:
            if i in self:
                self[i] += 1
            else:
                self[i] = 1

    def get_weighted_random_word(self):
        weight = self._get_random_weight()
        return self._get_random_item_by_weight(weight)[0]

    def _get_random_weight(self):
        weight_limit = sorted(self.items(), key=lambda x: x[1], reverse=True)[0][1]
        return random.randint(1, weight_limit)

    def _get_random_item_by_weight(self, weight):
        items = [i for i in self.items() if i[1] >= weight]
        return random.sample(items, 1)[0]
