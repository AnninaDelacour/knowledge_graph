from rdflib import Graph, Namespace, RDF, RDFS

def create_volleyball_ontology():
    graph = Graph()
    vbn = Namespace("http://example.org/volleyball#")
    graph.bind("vbn", vbn)

    # Classes
    graph.add((vbn.Person, RDF.type, RDFS.Class))
    graph.add((vbn.Athlete, RDF.type, RDFS.Class))
    graph.add((vbn.VolleyballPlayer, RDF.type, RDFS.Class))
    graph.add((vbn.Team, RDF.type, RDFS.Class))
    graph.add((vbn.Position, RDF.type, RDFS.Class))
    graph.add((vbn.Nationality, RDF.type, RDFS.Class))

    # Class Hierarchies
    graph.add((vbn.Athlete, RDFS.subClassOf, vbn.Person))
    graph.add((vbn.VolleyballPlayer, RDFS.subClassOf, vbn.Athlete))

    # Properties
    graph.add((vbn.hasName, RDF.type, RDF.Property))
    graph.add((vbn.hasName, RDFS.domain, vbn.Person))
    graph.add((vbn.hasName, RDFS.range, RDFS.Literal))

    graph.add((vbn.hasPosition, RDF.type, RDF.Property))
    graph.add((vbn.hasPosition, RDFS.domain, vbn.VolleyballPlayer))
    graph.add((vbn.hasPosition, RDFS.range, vbn.Position))

    graph.add((vbn.hasNationality, RDF.type, RDF.Property))
    graph.add((vbn.hasNationality, RDFS.domain, vbn.Person))
    graph.add((vbn.hasNationality, RDFS.range, vbn.Nationality))

    graph.add((vbn.hasHeight, RDF.type, RDF.Property))
    graph.add((vbn.hasHeight, RDFS.domain, vbn.VolleyballPlayer))
    graph.add((vbn.hasHeight, RDFS.range, RDFS.Literal))

    graph.add((vbn.hasJerseyNumber, RDF.type, RDF.Property))
    graph.add((vbn.hasJerseyNumber, RDFS.domain, vbn.VolleyballPlayer))
    graph.add((vbn.hasJerseyNumber, RDFS.range, RDFS.Literal))

    graph.add((vbn.playsFor, RDF.type, RDF.Property))
    graph.add((vbn.playsFor, RDFS.domain, vbn.VolleyballPlayer))
    graph.add((vbn.playsFor, RDFS.range, vbn.Team))

    return graph
