from models.word_completor import WordCompletor
from models.ngram_model import NGramLanguageModel
from models.text_suggestion import TextSuggestion

import pandas as pd


emails = pd.read_pickle("data/emails_tokens.pkl")
# for index, row in emails.head(3).iterrows():
#     print(row['cleaned_message'], row['tokens'], sep='\n')

#     print('/'*80)

dummy_corpus = emails['tokens'].tolist()[:5000]
print(dummy_corpus[5])

word_completor = WordCompletor(dummy_corpus)
n_gram_model = NGramLanguageModel(corpus=dummy_corpus, n=2)

text_suggestion = TextSuggestion(word_completor, n_gram_model)

print(word_completor.vocabulary[:50])


words, probs = word_completor.get_words_and_probs("abou")
print(words, probs)

words, probs = word_completor.get_words_and_probs("about")
print(words, probs)

text = ["how", "about"]
suggestions = text_suggestion.suggest_text(text, n_words=3)
print("Suggestions:", suggestions)