class NGramLanguageModel:
    def __init__(self, corpus, n):

        self.prev_words_next_count = {}
        for text in corpus:
            for i in range(len(text) - n):
                prev_words = text[i:i+n]
                prev_words = tuple(prev_words)
                next_word = text[i+n]

                if prev_words not in self.prev_words_next_count:
                    self.prev_words_next_count[prev_words] = {}
                if next_word not in self.prev_words_next_count[prev_words]:
                    self.prev_words_next_count[prev_words][next_word] = 0
                self.prev_words_next_count[prev_words][next_word] += 1

        self.n = n
        # print(self.prev_words_next_count)

    def get_next_words_and_probs(self, prefix: list) -> (List[str], List[float]):
        """
        Возвращает список слов, которые могут идти после prefix,
        а так же список вероятностей этих слов
        """
        prefix = tuple(prefix)
        if prefix not in self.prev_words_next_count:
            return [], []
        next_words_count = self.prev_words_next_count[prefix]
        # print(next_words_count)
        summ = sum(next_words_count.values())

        next_words, probs = [], []
        for next_word, count in next_words_count.items():
            next_words.append(next_word)
            probs.append(count / summ)

        return next_words, probs