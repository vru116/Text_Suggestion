from typing import Union
import numpy as np
from nltk.tokenize import word_tokenize


class TextSuggestion:
    def __init__(self, word_completor, n_gram_model):
        self.word_completor = word_completor
        self.n_gram_model = n_gram_model

    def suggest_text(self, text: Union[str, list], n_words=3, n_texts=1) -> list[list[str]]:
        """
        Возвращает возможные варианты продолжения текста (по умолчанию только один)
        
        text: строка или список слов – написанный пользователем текст
        n_words: число слов, которые дописывает n-граммная модель
        n_texts: число возвращаемых продолжений (пока что только одно)
        
        return: list[list[srt]] – список из n_texts списков слов, по 1 + n_words слов в каждом
        Первое слово – это то, которое WordCompletor дополнил до целого.
        """
        if not text: 
            return [[]]

        if isinstance(text, str):
            text = text.word_tokenize()
        
        last_word = text[-1]
        prefix = text[:-1]
        index_of_begin = len(prefix)

        words, probs = self.word_completor.get_words_and_probs(last_word)
        if not words:
            return [[]]

        top_i = np.argsort(probs)[::-1][:n_texts]
        cur_beams = {}
        for i in top_i:
            cur_beams[tuple(prefix + [words[i]])] = probs[i]
        # print(cur_beams)
        suggestions = dict()
        for cur_text in cur_beams.keys():
            if " ".join(cur_text[index_of_begin:]).strip() not in suggestions:
                suggestions[" ".join(cur_text[index_of_begin:]).strip()] = cur_beams[cur_text]

        for _ in range(n_words):
            # print(corpus)
            # print(suggestions)
            new_beams = {}
            for cur_text, prob in cur_beams.items():
                corpus = list(cur_text)
                prefix_for_ngram = corpus[len(corpus) - self.n_gram_model.n:]
                # print(prefix_for_ngram)
                # print('---')
                next_words, next_probs = self.n_gram_model.get_next_words_and_probs(prefix_for_ngram)
                # print(next_words, next_probs)
                if not next_words:
                    new_beams[cur_text] = prob
                    continue

                top_i = np.argsort(next_probs)[::-1][:n_texts]
                for i in top_i:
                    next_word = next_words[i]
                    new_prob = prob * next_probs[i]
                    new_beams[tuple(corpus + [next_word])] = new_prob
                
            cur_beams = sorted(new_beams.items(), key=lambda x: x[1], reverse=True)[:n_texts]
            cur_beams = dict(cur_beams)

            for cur_text in cur_beams.keys():
                if " ".join(cur_text[index_of_begin:]).strip() not in suggestions:
                    suggestions[" ".join(cur_text[index_of_begin:]).strip()] = cur_beams[cur_text]

        suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
        suggestions = dict(suggestions)
        suggestions = [sug.split() for sug in suggestions.keys()]
        return suggestions