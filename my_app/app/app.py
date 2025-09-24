import reflex as rx
import pandas as pd
from rxconfig import config

from models.word_completor import WordCompletor
from models.ngram_model import NGramLanguageModel
from models.text_suggestion import TextSuggestion

from data_loader import get_emails
from nltk.tokenize import word_tokenize


emails = get_emails()
# dummy_corpus = emails["tokens"].tolist()[:5000]
dummy_corpus = emails["tokens"].tolist()
# print(len(dummy_corpus))
word_completor = WordCompletor(dummy_corpus)
n_gram_model = NGramLanguageModel(corpus=dummy_corpus, n=2)
text_suggestion = TextSuggestion(word_completor, n_gram_model)

class State(rx.State):
    cur_text: str = ""
    cur_suggestions: list[list[str]] = [[]] 

    def set_text(self, event_value: str):
        self.cur_text = event_value
        self.get_suggestions()
        # print(f"suggestions = {self.cur_suggestions}")

    def get_suggestions(self):
        # print(self.cur_text)
        text_list = word_tokenize(self.cur_text)
        # print(text_list)
        suggestions = text_suggestion.suggest_text(text_list, n_words=3, n_texts=2)

        self.cur_suggestions = []
        for sugs in suggestions:
            # cur_list = []
            # for i in range(1, len(sugs) + 1):
            #     cur_list.append(" ".join(sugs[:i]))
            # self.cur_suggestions.append(cur_list)
            self.cur_suggestions.append(" ".join(sugs))
    
    def click_suggestion(self, suggestion: str):
        # print(f"suggestions1 = {self.cur_suggestions}")
        # print(f"suggestion = {suggestion}")
        suggestion = str(suggestion).strip()

        words = word_tokenize(self.cur_text)
        if words:
            words = words[:-1]

        new_words = word_tokenize(suggestion)
        words.extend(new_words)

        self.cur_text = " ".join(words).strip()
        self.cur_suggestions = []
        self.get_suggestions()


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Text Suggestion", size="7", color="green", text_align="center"),
            rx.text("Введите текст, и система подскажет продолжение."),

            rx.input(
                placeholder="Введите текст...",
                value=State.cur_text,
                on_change=State.set_text,
                style={"width": "100%", "height": "40px", "font-size": "16px"}
            ),

            rx.vstack(
                rx.foreach(
                    State.cur_suggestions,
                    lambda suggestion: rx.button(
                        suggestion,
                        on_click=lambda *args, s=suggestion: State.click_suggestion(s)
                    )
                ),
                spacing="2",
            ),   
        ),
        padding="4",
    )

app = rx.App()
app.add_page(index, title="Text Suggestion")