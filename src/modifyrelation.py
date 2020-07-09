#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prototypical/unfinished module to modify both object and data properties on the basis of string input"""

import datetime
from owlready2 import get_ontology
from owlready2 import IRIS
from owlready2 import default_world
import rdflib
import preprocess as ppr

IRI = "http://david.org/informationmodel.owl#"
ONTOFILE = "populated-information-model.owl"
INSTANCE1 = "Delphi-Simulation.zip"
INSTANCE2 = "Band.zip" 
RELATION = "related_to"

def modify_relation(instance1, relation, instance2, mode):
    """add or remove the relation between two instances"""
    #TODO possibly prefilter class; ensure consistency between type of instance2 and range of data property to be modified
    onto = get_ontology(ONTOFILE).load()
    with onto:
        instances = list(onto.individuals())
        object_properties = list(onto.object_properties())
        data_properties = list(onto.data_properties())
        try:
            instance1 = instance1.split(".",1)
            instance1 = str(instance1[1])
        except:
            instance1 = str(instance1[0])
        iri_instance1 = IRIS[IRI + instance1]
        try:
            relation = relation.split(".",1)
            relation = str(relation[1])
        except:
            relation = str(relation[0])
        iri_relation = IRIS[IRI + relation]
        if (iri_instance1 not in instances):
            print("instance1: " + instance1 + " not recognized. Please check existence in " + ONTOFILE)
            return 0
        if ((iri_relation not in object_properties) and (iri_relation not in data_properties)):
            print("relation: " + relation + " not recognized. Please check existence in " + ONTOFILE)
            return 0
        if (mode==1 or mode==2):
            try:
                instance2 = instance2.split(".",1)
                instance2 = str(instance2[1])
            except:
                instance2 = str(instance2[0])
            iri_instance2 = IRIS[IRI + instance2]
            if (iri_instance2 not in instances):
                print("instance2: " + instance2 + " not recognized. Please check existence in " + ONTOFILE)
                return 0
            if (iri_relation in data_properties):
                print(relation + " is a data property. Switch mode to 3 or 4, or provide a valid object property.")
                return 0
            try:
                relation_domain = iri_relation.domain
                relation_range = iri_relation.range
            except:
                print("Relation domain/range can not be retrieved. Please check whether " + relation + " is a valid object property.")
                return 0
            if relation_domain:
                relation_domain_ind = list(onto.search(type = relation_domain))
            else:
                relation_domain_ind = []
            if relation_range:
                relation_range_ind = list(onto.search(type = relation_range))
            else:
                relation_range_ind = []
            if relation_domain_ind and (iri_instance1 not in relation_domain_ind):
                print(instance1 + " is not within in the domain of " + str(iri_relation) + " The relation can thus not be created.")
                return 0
            if relation_range_ind and (iri_instance2 not in relation_range_ind):
                print(instance2 + " is not within in the range of " + str(iri_relation) + " The relation can thus not be created.")
                return 0

        if (mode==3 or mode==4):
            if iri_relation in object_properties:
                print(relation + " is a object property. Switch mode to 1 or 2, or provide a valid data property.")
                return 0
            if iri_relation.range[0] == bool:
                instance2 = str(bool(instance2))
                instance2 = [str('"' + instance2 + '"')]
                datatype = ["^^xsd:bool"]
            elif iri_relation.range[0] == float:
                instance2 = str(float(instance2))
                instance2 = [str('"' + instance2 + '"')]
                datatype = ["^^xsd:float"]
            elif iri_relation.range[0] == int:
                instance2 = str(int(instance2))
                instance2 = [str('"' + instance2 + '"')]
                datatype = ["^^xsd:int"]
            elif iri_relation.range[0] == str:
                instance2 = ppr.pp_str(instance2)
                instance2 = [str(':' + instance2)]
            elif iri_relation.range[0] == datetime.datetime:
                instance2 = [str('"' + instance2 + '"')]
                datatype = ["^^xsd:dateTime"]
            instance2.insert(0,"?x")
            datatype.insert(0,"")
        else:
            instance2 = [str(":" + instance2)]
            datatype = [""]

        queries = []
        query_forms = ["ASK WHERE","INSERT DATA","DELETE DATA","SELECT DISTINCT ?x WHERE"]
        for i in range(0,len(instance2)):
            for j in range(0,len(query_forms)):
                query = """PREFIX : <http://david.org/informationmodel.owl#>
                           """ + query_forms[j] + """ {
                           :""" + instance1 + """ :""" + relation + """ """ + instance2[i] + datatype[i] + """ .
                           }"""
                queries.append(query)
        
        graph = default_world.as_rdflib_graph()

        if ((mode==1) or (mode==2)):
            query = str(queries[0])
        elif ((mode==3) or (mode==4)):
            query = str(queries[4])
        exists = list(graph.query(query))

        if ((mode==1) and (exists[0]==True)):
            print(instance1 + " is already related via relation " + relation + " to " + str(instance2[0]))
        elif ((mode==1) and not (exists[0]==True)):
            graph.update(queries[1])
            print(instance1 + " is now related via relation " + relation + " to " + str(instance2[0]))
        elif ((mode==2) and (exists[0]==True)):
            graph.update(queries[2])
            print("The relation " + instance1 + " " + relation + " " + str(instance2[0]) + " has been removed.")
        elif ((mode==2) and not (exists[0]==True)):
            print(instance1 + " is not related via " + relation + " to " + str(instance2[0]) + " The relation can thus not be removed.")
        elif ((mode==3) and (exists[0]==True)):
            print(instance1 + " is already related via data property " + relation + " to " + instance2[1])
        elif ((mode==3) and not (exists[0]==True)):
            rel_exists = list(graph.query(queries[3]))
            if rel_exists:
                query = """PREFIX : <http://david.org/informationmodel.owl#>
                           DELETE {
                           :""" + instance1 + """ :""" + relation + """ ?x .
                           }
                           INSERT {
                           :""" + instance1 + """ :""" + relation + """ """ + instance2[1] + """""" + datatype[1] + """ .
                           }
                           WHERE {
                           :""" + instance1 + """ :""" + relation + """ ?x .
                           }"""
                graph.update(query)
                print("Replaced existing data property of " + relation + " of " + instance1)
            else:
                graph.update(queries[5])
            print(instance1 + " is now related via data property " + relation + " to " + instance2[1])
        elif ((mode==4) and (exists[0]==True)):
            graph.update(queries[6])
            print(instance1 + " relation via " + relation + " to " + instance2[1] + " has been removed.")
        elif ((mode==4) and not (exists[0]==True)):
            print(instance1 + " is not related via " + relation + " to " + instance2[1] + " The relation can thus not be removed.")

    onto.save(file = ONTOFILE)

def list_relations():
    onto = get_ontology(ONTOFILE).load()
    with onto:
        relations = list(onto.object_properties())
    return relations

def main():
    modify_relation(INSTANCE1,RELATION,INSTANCE2,1)

if __name__ == "__main__":
    main()
