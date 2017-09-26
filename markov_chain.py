from dictogram import Dictogram


class MarkovChain:
    """order - величина статистического окна."""
    def __init__(self, order=1):
        self.model = {}
        self.N = order

    def parse_and_add(self, string):
        """Преобразует строку в набор набор последовательностей и добавляет их в статистику."""
        data = []
        words = [w.strip() for w in string.split()]
        is_end_of_sentence = False
        for word in words:
            data.append(word)
            if is_end_of_sentence:
                self.add(data)
                data = [word]
                is_end_of_sentence = False
            if word[-1] in ('.', '?', '!'):
                is_end_of_sentence = True
        self.add(data)

    def add(self, data):
        """Добавляет набор слов в статистику."""
        for i in range(len(data) - self.N):
            window = tuple(data[i: self.N + i])
            if i == 0:
                self._add_start_window(window)
            if window not in self.model:
                self.model[window] = Dictogram([data[i + self.N]])
            else:
                self.model[window].update([data[i + self.N]])

    def generate_sentence(self, length):
        """Возвращает сгенерированное на основе статистики предложение."""
        window = self._get_start_window()
        window_str = ' '.join(window)
        sentence = [window_str]
        length -= len(window_str)
        while True:
            need_capitalize = sentence[-1][-1] in ('?', '!', '.')
            if window not in self.model:
                return self._get_joined_sentence(sentence)
            word = self.model[window].get_weighted_random_word()
            length = self._get_length_limit(length, word)
            if length < 0:
                return self._get_joined_sentence(sentence)
            sentence.append(word)
            window = tuple([sentence[-self.N]])
            if need_capitalize:
                sentence[-1] = sentence[-1].capitalize()

    def _get_start_window(self):
        """Возвращает выбранное на основе статистических весов начальное окно последовательности."""
        return self.model['START'].get_weighted_random_word()

    def _add_start_window(self, window):
        """Добавляет в статистику окно начальных слов для генерации последовательности."""
        if 'START' not in self.model:
            self.model['START'] = Dictogram([window])
        else:
            self.model['START'].update([window])

    @staticmethod
    def _get_length_limit(length, word):
        """Возвращает остаток лимита длинны строки."""
        length -= len(word) + 1  # 1 - потенциальный пробел после преобразования в строку
        # Проверяем особый случай, когда достигнута максимальная длинна строки,
        # но в конце предложения не хватает завершающего знака препинания
        if length == 0:
            if word[-1] in ('.', '?', '!'):
                return length
            return length - 1
        return length

    @staticmethod
    def _get_joined_sentence(sentence):
        """Возвращает преобразованное из списка в строку предложение."""
        while sentence[-1][-1] in (',', ':', ';'):
            sentence[-1] = sentence[-1][:-1]
        if sentence[-1][-1] not in ('.', '?', '!'):
            sentence[-1] += '.'
        sentence[0] = sentence[0].capitalize()
        return ' '.join(sentence)
