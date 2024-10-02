import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace

def create_volleyball_ontology():
    df = pd.read_csv('Spielerinnendaten.csv')

    g = Graph()

    vbn = Namespace("http://example.org/volleyball#")
    g.bind("vbn", vbn)

    RDFS_NS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    g.bind("rdfs", RDFS_NS)

    team_uri = URIRef(f"http://example.org/volleyball#Nationalteam")
    stadion_uri = URIRef(f"http://example.org/volleyball#ExampleStadion")

    g.add((team_uri, RDF.type, vbn.Team))
    g.add((stadion_uri, RDF.type, vbn.Stadion))

    g.add((stadion_uri, vbn.hasStadionName, Literal("Example Stadion")))
    g.add((stadion_uri, vbn.hasStadionAdress, Literal("Example Adress")))
    g.add((team_uri, vbn.hasTeamName, Literal("Nationalmannschaft")))
    g.add((team_uri, vbn.hasHomeStadion, stadion_uri))

    for index, row in df.iterrows():
        player_uri = URIRef(f"http://example.org/volleyball#player_{index+1}")
        
        g.add((player_uri, RDF.type, vbn.VolleyballPlayer))
        g.add((player_uri, vbn.hasName, Literal(row['Name'])))
        g.add((player_uri, vbn.hasHeight, Literal(row['Groesse'])))
        g.add((player_uri, vbn.hasJerseyNumber, Literal(row['Dressnummer'])))
        g.add((player_uri, vbn.playsFor, team_uri))
        
        nationality_uri = URIRef(f"http://example.org/volleyball#nationality_{row['Nationalitaet']}")
        g.add((nationality_uri, RDF.type, vbn.Nationality))
        g.add((player_uri, vbn.hasNationality, nationality_uri))
        
        position_uri = URIRef(f"http://example.org/volleyball#position_{row['Position']}")
        g.add((position_uri, RDF.type, vbn.Position))
        g.add((player_uri, vbn.hasPosition, position_uri))

    g.serialize(destination="volleyball_players.ttl", format="turtle")

    return g
