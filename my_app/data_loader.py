from functools import lru_cache
import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@lru_cache
def get_emails():
    return pd.read_pickle(os.path.join(BASE_DIR, "data", "emails_tokens.pkl")).head(5000)
