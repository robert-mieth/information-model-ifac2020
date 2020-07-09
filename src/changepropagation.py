#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SPARQL query for finding stakeholders that should be notified of changes"""

import executequery as xq

ONTOFILE = "file://./xppu-information-model.owl"

# parameters
ONTOFILE = "populated-information-model.owl"
INFOCONC_CHANGED = "CraneDrawing"

def confquery(infoconc_changed):
    """configures SPARQL query to retrieve infotype contained in infoconc_changed and subscribed actors """
    query = """PREFIX : <http://david.org/informationmodel.owl#>
            SELECT DISTINCT ?info ?role ?actor WHERE {
                ?info rdf:type/rdfs:subClassOf* :information .
                ?actor rdf:type/rdfs:subClassOf* :actor .
                ?actor :subscribes :""" + infoconc_changed + """ .
                :""" + infoconc_changed + """ :stored_as ?doc_format .
                ?doc_format :can_format ?info .
                ?doc_format :has_role ?role .
            }"""
    return query

def returnresults(infoconc_changed=INFOCONC_CHANGED):
    li = xq.executequery(ONTOFILE, confquery(infoconc_changed))
    for i in li:
        print("notify",i[2],"that",i[0],"with role",i[1],"has been changed")


def main(infoconc_changed):
    returnresults()


if __name__ == "__main__":
    main(INFOCONC_CHANGED)
