import re
from collections import defaultdict
from nltk.tokenize import word_tokenize

def clean_text(text):
    text = re.sub(r'\W+', ' ', text)
    return text.lower()

def build_inverted_index(docs):
    inverted_index = defaultdict(list)
    for doc_id, doc_fields in enumerate(docs):
        combined_fields = " ".join([str(field) for field in doc_fields])
        tokens = word_tokenize(clean_text(combined_fields))
        for token in tokens:
            if doc_id not in inverted_index[token]:
                inverted_index[str(token)].append(doc_id)
    return inverted_index
