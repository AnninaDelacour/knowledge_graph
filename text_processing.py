import re
from collections import defaultdict
from nltk.tokenize import word_tokenize
from rdflib import Graph, Literal, URIRef
from ontology_graph import create_volleyball_ontology


def clean_text(text):
    text = re.sub(r'\W+', ' ', text)
    return text.lower()
    

def build_inverted_index(docs):
    '''
    Die bestehende Funktion wird nun erweitert, um die Ontologie-Daten zu integrieren.
    Es werden alle Tripel (s = Subjekt = Instanz o Klasse in Ontologie, 
    p = Prädikat = Eigenschaft d. Subjekts, 
    o = Objekt = Literal oder Referenz auf andere Instanz) durchlaufen.
    Wenn o ein Literal ist, wird es bereinigt und in den Inverted Index gespeichert. Ist es eine Referenz, 
    wird der Namespace abgeschnitten und dann in den Index eingefügt.
    '''
    inverted_index = defaultdict(list)
    
    graph = create_volleyball_ontology()
    namespace = "http://example.org/volleyball#"
    
    for doc_id, doc_fields in enumerate(docs):
        combined_fields = " ".join([str(field) for field in doc_fields])
        tokens = word_tokenize(clean_text(combined_fields))
        
        for token in tokens:
            if doc_id not in inverted_index[token]:
                inverted_index[str(token)].append(doc_id)
        
        for s, p, o in graph.triples((None, None, None)):
            if isinstance(o, Literal):
                token = clean_text(str(o))
                if doc_id not in inverted_index[token]:
                    inverted_index[token].append(doc_id)
            elif isinstance(o, URIRef):
                token = clean_text(str(o).replace(str(namespace), ''))
                if doc_id not in inverted_index[token]:
                    inverted_index[token].append(doc_id)
    
    return inverted_index
