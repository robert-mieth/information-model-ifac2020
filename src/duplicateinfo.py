#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SPARQL query for identifying duplicate information in the information model"""

import executequery as xq
import datetime

ONTOFILE = "file://./populated-information-model.owl"
QUERY = """PREFIX : <http://david.org/informationmodel.owl#>
        SELECT DISTINCT ?info ?role ?conc ?carrier WHERE {
        ?info a/rdfs:subClassOf* :information .
        ?role a/rdfs:subClassOf* :role .
        ?carrier :captures ?conc .
        ?conc :stored_as ?doc_format .
        ?doc_format :has_role ?role .
        ?doc_format :can_format ?info .
        {
            SELECT ?info ?role (COUNT (?concs) AS ?count) WHERE {
                ?concs :stored_as ?doc_format .
                ?doc_format :has_role ?role .
                ?doc_format :can_format ?info .
            }
            GROUP BY ?info ?role
        }
        FILTER (?count > 1)}"""

QUERY2 = """PREFIX : <http://david.org/informationmodel.owl#>
        SELECT DISTINCT ?x ?y ?pathx ?pathy WHERE {
        ?x :timestamp_modification ?ts1 .
        ?y :timestamp_modification ?ts2 .
        ?x :has_filesize ?fs1 .
        ?y :has_filesize ?fs2 .
        ?x :has_path ?pathx .
        ?y :has_path ?pathy .
        FILTER (?ts1 = ?ts2 && ?fs1 = ?fs2 && ?x != ?y)}"""

def printresults(li):
    """print query results in an easily interpretable way"""
    print("duplicate info:")
    print(li[0][0],"with role",li[0][1],"contained in",li[0][2],"on",li[0][3])
    for a, b in zip(li[1:], li):
        if (a[0] == b[0] and a[1] == b[1]):
            print("\t",a[0],"with role",a[1],"also contained in",a[2],"on",a[3])
        else:
            print(a[0],"with role",a[1],"contained in",a[2],"on",a[3])

def printresults_alt(li):
    """print query results in an easily interpretable way"""
    print("duplicate info:")
    for a, b in zip(li[1:], li):
        print("\t",a[0],"possibly duplicate of",a[1],"\n\tPath 1",a[2],"Path2",a[3])


def main():
    printresults(xq.executequery(ONTOFILE, QUERY))
    #printresults_alt(xq.executequery(ONTOFILE, QUERY2))


if __name__ == "__main__":
    main()
