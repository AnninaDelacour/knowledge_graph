from text_processing import clean_text
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import math
from collections import Counter
import pandas as pd

def calculate_tf(doc):
    tokens = word_tokenize(clean_text(doc))
    total_tokens = len(tokens)
    tf = Counter(tokens)
    return {token: count / total_tokens for token, count in tf.items()}

def calculate_idf(documents, inverted_index):
    N = len(documents)
    idf = {}
    for token in inverted_index:
        df = len(inverted_index[token])
        idf[token] = math.log(N / (1 + df))
    return idf

def calculate_tfidf(documents, inverted_index):
    idf = calculate_idf(documents, inverted_index)
    tfidf_documents = []
    
    for doc_fields in documents:
        combined_fields = " ".join([str(field) for field in doc_fields])
        tf = calculate_tf(combined_fields)
        tfidf = {token: tf[token] * idf.get(token, 0) for token in tf}
        tfidf_documents.append(tfidf)
    
    all_tokens = sorted(set(token for tfidf in tfidf_documents for token in tfidf))
    tfidf_df = pd.DataFrame(0.0, index=range(len(documents)), columns=all_tokens)
    
    for doc_id, tfidf in enumerate(tfidf_documents):
        for token, value in tfidf.items():
            tfidf_df.at[doc_id, token] = value
    
    return tfidf_df

def search(tfidf_df, search_term):
    search_term = search_term.lower()
    
    if " and " in search_term:
        terms = search_term.split(" and ")
        operator = "AND"
    elif " or " in search_term:
        terms = search_term.split(" or ")
        operator = "OR"
    else:
        terms = [search_term]
        operator = None

    results = pd.DataFrame()

    for term in terms:
        term = term.strip()
        if term in tfidf_df.columns:
            ranked_docs = tfidf_df[term].sort_values(ascending=False)
            ranked_docs = ranked_docs[ranked_docs != 0]
            if results.empty:
                results = ranked_docs.to_frame()
            else:
                if operator == "AND":
                    results = results.merge(ranked_docs.to_frame(), left_index=True, right_index=True, how='inner')
                elif operator == "OR":
                    results = results.merge(ranked_docs.to_frame(), left_index=True, right_index=True, how='outer')
        else:
            print(f"'{term}' not found in player data.")
            return
    
    if operator == "AND":
        results['score'] = results.min(axis=1)
    elif operator == "OR":
        results['score'] = results.max(axis=1)
    else:
        results['score'] = results.iloc[:, 0]

    results = results[['score']].sort_values(by='score', ascending=False)
    
    if not results.empty:
        print(results)
    else:
        print("No results found.")
