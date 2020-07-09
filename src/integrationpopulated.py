#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calls functions in filecrawler, informationmodel, instancemodel and creates ontology"""

import filecrawler
import informationmodel
import instancemodel

IRI = "http://david.org/informationmodel.owl"
METAFILE = "information-model.owl"
INSTANCEFILE = "populated-information-model.owl"
PATH = "D:\\xppu_data"

def update():
    """Updates the populated-information-model"""
    #CAVEAT overwrites manual changes to crawled data properties
    instancemodel.FILES = filecrawler.crawl(PATH)
    instancemodel.instancemodel_population(INSTANCEFILE, INSTANCEFILE)
    instancemodel.verify_existence(INSTANCEFILE)


def main():
    """Calls fc_files, informationmodel, instancemodel and creates OWL ontology"""
    informationmodel.im_informationmodel(IRI, METAFILE)
    instancemodel.FILES = filecrawler.crawl(PATH)
    instancemodel.instancemodel_population(IRI, INSTANCEFILE)


if __name__ == "__main__":
    main()
    #update()