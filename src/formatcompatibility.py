#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SPARQL query for finding information carriers that cannot be accessed with the tools available,
    either bc the company does not have appropriate licenses or bc there is no appropriate tool"""

import executequery as xq

# parameters
ONTOFILE = "file://./populated-information-model.owl"
ORGANIZATION = "TUM"

QUERY = """PREFIX : <http://david.org/informationmodel.owl#>
        SELECT DISTINCT ?conc ?tool ?format WHERE {
        ?conc a/rdfs:subClassOf* :information_concretization ;
            :stored_as ?format .
        OPTIONAL { ?tool :supports ?format . }
        FILTER NOT EXISTS {
            :""" + ORGANIZATION + """ :has_license_for/:supports ?format .
        }
        }"""

def returnresults():
    res = xq.executequery(ONTOFILE, QUERY)
    return res

def printresults():
    res = returnresults()
    for i in res:
        if not i[1]:
            print(i[0], "- no tool available for format ", i[2])
    for i in res:
        if i[1]:
            print(i[0], "- no license available for tool", i[1])


def main():
    printresults()


if __name__ == "__main__":
    main()
