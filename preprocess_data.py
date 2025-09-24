from utils.preprocessing import clean_email
from nltk.tokenize import word_tokenize
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

emails = pd.read_csv("data/emails.csv")

emails['cleaned_message'] = emails['message'].progress_apply(clean_email)
emails['tokens'] = emails['cleaned_message'].progress_apply(word_tokenize)

emails.to_pickle("data/emails_tokens.pkl")