#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SPARQL queries for listing members of the ontology"""

import executequery as xq

ONTOFILE = "file://./populated-information-model.owl"

def confquery_classes(parent="owl:Thing"):
    """configures SPARQL query to retrieve all subclasses of given parent"""
    query = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX : <http://david.org/informationmodel.owl#>
            SELECT DISTINCT ?class WHERE {
            ?class rdfs:subClassOf* """ + parent + """ .
            }"""
    return query

def confquery_instances(parent="owl:Thing"):
    """configures SPARQL query to retrieve all instances of given parent and its subclasses"""
    query = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX : <http://david.org/informationmodel.owl#>
            SELECT DISTINCT ?instance WHERE {
            ?instance a/rdfs:subClassOf* """ + parent + """ .
            }"""
    return query

def find_classes(parent="owl:Thing"):
    """returns all subclasses of given parent"""
    return(xq.executequery(ONTOFILE, confquery_classes(parent)))

def find_instances(parent="owl:Thing"):
    """returns all instances of given parent and its subclasses"""
    return(xq.executequery(ONTOFILE, confquery_instances(parent)))


def main():
    print(find_classes())
    #print(find_instances())


if __name__ == "__main__":
    main()
