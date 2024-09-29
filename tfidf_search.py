from text_processing import clean_text
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import math
from collections import Counter
import pandas as pd
from ontology_graph import create_volleyball_ontology


''' TF Berechnung '''
def calculate_tf(doc):
    tokens = word_tokenize(clean_text(doc))
    total_tokens = len(tokens)
    tf = Counter(tokens)
    return {token: count / total_tokens for token, count in tf.items()}

''' IDF Berechnung '''
def calculate_idf(documents, inverted_index):
    N = len(documents)
    idf = {}
    for token in inverted_index:
        df = len(inverted_index[token])
        idf[token] = math.log(N / (1 + df))  # IDF berechnet die Häufigkeit eines Tokens im Inverted Index
    return idf

''' TF-IDF Berechnung '''
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


''' Formatiert die Ausgabe des Search Results und macht es etwas "schöner" '''
def format_search_results(results, original_df):
    if not results.empty:
        doc_ids = results.index
        formatted_results = original_df.iloc[doc_ids]
        
        # Die zuvor verknüpften Dokument-IDs werden mit den Daten verknüpft und relevante Daten ausgegeben
        formatted_results = formatted_results[['Name', 'Position', 'Groesse']]
        formatted_results['score'] = results['score']
        
        print(formatted_results.to_string(index=False))
    else:
        print("Search result: No results found.")


def search(tfidf_df, search_term, original_df):
    search_term = search_term.replace(" AND ", " and ").replace(" OR ", " or ").lower()
    
    graph = create_volleyball_ontology()
    namespace = "http://example.org/volleyball#"
    
    results = pd.DataFrame()
    
    # Splitted die Query auf, um and oder or zu finden
    if " and " in search_term:
        terms = search_term.split(" and ")
        operator = "AND"
    elif " or " in search_term:
        terms = search_term.split(" or ")
        operator = "OR"
    else:
        terms = search_term.split()  # Bei Mehrwortanfragen ohne Operator wird es in einzelne Begriffe gesplittet
        operator = None

    # Suche für jeden Suchbegriff
    for term in terms:
        term = term.strip()  # Um Leerzeichen zu entfernen
        found_in_ontology = False

        # Prüft hier, ob der Begriff in der Ontologie vorkommt
        for s, p, o in graph.triples((None, None, None)):
            if clean_text(str(o)) == term or clean_text(str(p).replace(str(namespace), '')) == term:
                found_in_ontology = True
                break
        
        if found_in_ontology:
            print(f"'{term}' found in ontology.")
            # HIER KÖNNTE SPARQL-CODE STEHEN :-)
        elif term in tfidf_df.columns:
            ranked_docs = tfidf_df[term].sort_values(ascending=False)
            ranked_docs = ranked_docs[ranked_docs != 0]
            if results.empty:
                results = ranked_docs.to_frame()  # Fügt die Resultate dem Dataframe hinzu
            else:
                # OR: Äußerer Merge, um die Vereinigung der Ergebnisse zu erhalten
                if operator == "OR":
                    results = results.merge(ranked_docs.to_frame(), left_index=True, right_index=True, how='outer')
                # AND: Innerer Merge, um die Schnittmenge der Ergebnisse zu erhalten
                elif operator == "AND":
                    results = results.merge(ranked_docs.to_frame(), left_index=True, right_index=True, how='inner')
                # Wenn kein Operator vorhanden ist (z.B. bei "Nicole Aufspiel"), kombiniere die Ergebnisse
                else:
                    results = results.merge(ranked_docs.to_frame(), left_index=True, right_index=True, how='inner')
        else:
            print(f"'{term}' not found in player data.")
            return
    
    # Score-Berechnung basierend auf AND/OR oder bei einfacher Mehrwortsuche
    if operator == "AND":
        results['score'] = results.min(axis=1)  # Bei AND wird das Minimum als finaler Score verwendet
    elif operator == "OR":
        results['score'] = results.max(axis=1)  # Bei OR hingegen das Maximum
    else:
        results['score'] = results.min(axis=1)  # Bei Mehrwortanfragen ohne Operator (wie "Nicole Aufspiel") wird die Schnittmenge verwendet

    # Sortiert die Resultate absteigend
    results = results[['score']].sort_values(by='score', ascending=False)

    format_search_results(results, original_df)


