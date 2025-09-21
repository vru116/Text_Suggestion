from tokenizers import normalizers
from tokenizers.normalizers import NFD, StripAccents, Lowercase, Strip

import re

from tqdm import tqdm
tqdm.pandas() 

normalizer = normalizers.Sequence([NFD(), StripAccents(), Strip()])


def clean_email(text):
    if "X-FileName:" in text:
        new_text = text.split('X-FileName:', 1)[1]
        new_text = new_text.split('\n', 1)[1] 
    else:
        new_text = text

    lines = new_text.split('\n')
    new_lines = []
    for line in lines:       
        line = line.replace('>', '')
        line = line.lower()

        if (line.startswith('from:') or
            line.startswith('to:') or
            line.startswith('subject:') or
            line.startswith('cc:') or
            line.startswith('sent:') or
            'forwarded by' in line or
            'original message' in line or
            '----' in line or
            '@' in line
            ):
            continue

        new_lines.append(line)

    new_text = "\n".join(new_lines)

    new_text = re.sub(r'<[^<]+?>', '', new_text)
    new_text = re.sub(r'http\S+', '', new_text)
    new_text = re.sub(r'[^a-zA-Z0-9\s]', '', new_text)
    new_text = re.sub(r'[^\w\s]', '', new_text)
    new_text = re.sub(r'\+?\d[\d\-\s]{6,}', '', new_text)
    new_text = re.sub(r'\n\s*\n', '\n', new_text)
    
    new_text = normalizer.normalize_str(new_text)
    return new_text