#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SPARQL queries for finding information concretizations and carriers that capture information"""

import executequery as xq
import datetime

ONTOFILE = "populated-information-model.owl"

def confquery(infokind, role):
    query = """PREFIX : <http://david.org/informationmodel.owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT DISTINCT ?ic ?carrier  WHERE {
                ?ic :stored_as ?doc_format .
                ?doc_format :can_format ?info .
                ?info a/rdfs:subClassOf* """ + infokind + """ .
                ?doc_format :has_role """ + role + """ .
                ?carrier :captures ?ic .
            }"""
    return query

def confquery_fs(file_size):
    query = """PREFIX : <http://david.org/informationmodel.owl#>
            SELECT DISTINCT ?information_concretization ?x WHERE {
            ?information_concretization :has_filesize ?x .
            FILTER (?x > """ + file_size + """)
            }"""
    return query

def confquery_system(infokind, role, system):
    query = """PREFIX : <http://david.org/informationmodel.owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT ?ic ?carrier  WHERE {
                ?ic a :information_concretization .
                ?ic :describes :""" + system + """ .
                ?ic :stored_as ?doc_format .
                ?doc_format :can_format ?infotype .
                ?infotype a/rdfs:subClassOf* :""" + infokind + """ .
                ?doc_format :has_role :""" + role + """ .
                ?carrier :captures ?ic .
                ?carrier a :information_carrier .
                }"""
    return query

def returnresult(infokind, role):
    li = xq.executequery(ONTOFILE, confquery(infokind, role))  
    printresults(li)
    return li  

def returnresults_fs(file_size):
    li = xq.executequery(ONTOFILE, confquery_fs(file_size))  
    printresults_fs(li)
    return li

def returnresults_system(infokind, role, system):
    li = xq.executequery(ONTOFILE, confquery_system(infokind, role, system))  
    printresults_system(li)
    return li  

def printresults(li):
    """print query results in an easily interpretable way"""
    print("info is available in:")
    for i in li:
        print(i[0],"stored here:",i[1])

def printresults_fs(li):
    """print query results in an easily interpretable way"""
    print("info is available in:")
    for i in li:
        print(i[0],"has filesize",i[1],"bytes")

def printresults_system(li):
    """print query results in an easily interpretable way"""
    print("info is available in:")
    for i in li:
        print(i[0],"stored here:",i[1])


def main():
    returnresult(infokind=":behavioral_information", role=":prescriptive_role")
    #returnresults_fs(file_size="87741239")
    #returnresults_system(infokind="structural_information", role="prescriptive_role", system="Crane")



if __name__ == "__main__":
    main()