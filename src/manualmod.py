#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manually modify the populated information model; includes functions not yet supported by simplegui"""

from owlready2 import get_ontology
from owlready2 import IRIS
from owlready2 import Thing
from owlready2 import destroy_entity
import types
from preprocess import pp_str

IRI = "http://david.org/informationmodel.owl#"
INSTANCEFILE = "file://populated-information-model.owl"
INSTANCEFILEMOD = "populated-information-model.owl"
IC = "Hauptfilm.mp4"
LANGUAGE = "Spanish"
SYSTEM = "Crane"

def list_relations():
    onto = get_ontology(INSTANCEFILE).load()
    with onto:
        relations = onto.object_properties()
    return relations

def list_instances():
    onto = get_ontology(INSTANCEFILE).load()
    with onto:
        entities = list(onto.individuals())
    return entities

def insert_relation(instance1, relation, instance2):
    onto = get_ontology(INSTANCEFILE).load()
    with onto:
        iris_ics = list(onto.individuals())
        iris_relations = list(onto.object_properties())
        iris_instance1 = IRIS[IRI + str(instance1)]
        iris_instance2 = IRIS[IRI + str(instance2)]
        relation = str(relation.split('.',1)[-1])
        iris_relation = IRIS[IRI + str(relation)]
        try:
            relation_domain = iris_relation.domain[0]
            relation_range = iris_relation.range[0]
            if iris_instance1 not in list(relation_domain.instances()) :
                print(instance1 + " is not in the domain of " + relation + ". Exited.")
                return 0
            if iris_instance2 not in list(relation_range.instances()):
                print(instance2 + " is not in the range of " + relation + ". Exited.")
                return 0
        except:
            pass    
        if (iris_instance1 in iris_ics):
            if (iris_instance2 in iris_ics):
                if (iris_relation in iris_relations):
                    try:
                        getattr(iris_instance1, str(relation)).append(iris_instance2)
                        print(instance1 + " " + relation + " " + instance2 + " inserted.")
                    except:
                        print("Error. Check if relation already exists.")
                else:
                    print("Relation: " + relation + " not recognized.")
            else:
                print(str(instance2) + " not recognized.")
        else:
            print(str(instance1) + " not recognized.")

    onto.save(file=INSTANCEFILEMOD)

def create_instance(name, parent):
    onto = get_ontology(INSTANCEFILE).load()
    with onto:
        iris_classes = onto.classes()
        iris_instances = onto.individuals()
        name = pp_str(name)
        iris_name = IRIS[IRI+ str(name)]
        iris_parent = IRIS[IRI + str(parent)]
        if (iris_parent in iris_classes):
            if (iris_name not in iris_instances):
                try:
                    classes = {"klass": iris_parent}
                    classes["klass"](name)
                    print("Instance: " + str(name) + " as " + str(iris_parent) + " created.")
                except:
                    print("Error. Could not create instance.")
            else:
                print("Entity with name: " + str(name) + " already exists in ontology.")
        else:
            print(str(parent) + " not recognized.")
    onto.save(file=INSTANCEFILEMOD)

def remove_entity(name):
    onto = get_ontology(INSTANCEFILE).load()
    with onto:
        try:
            name = str(name.split('.',1)[1])
        except:
            pass
        name = IRIS[IRI + str(name)]
        destroy_entity(name)
        print("Entity: " + str(name) + " removed.")
    onto.save(file=INSTANCEFILEMOD)


def main():
    insert_relation("Robert","subscribes","Doppelrutsche_AIS.dwg")
    #create_instance("Crane", "system")
    #remove_entity("Robert")


if __name__ == "__main__":
    main()