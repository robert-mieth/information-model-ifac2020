#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""module for loading an ontology, running a SPARQL query, and returning the results as a list"""

from owlready2 import get_ontology
from owlready2 import default_world
import rdflib
import types

def executequery(pathtoonto, query):
    """load ontology, query it, and return results as list"""
    onto = get_ontology(pathtoonto).load()
    graph = default_world.as_rdflib_graph()
    li = list(graph.query_owlready(query))
    return li
