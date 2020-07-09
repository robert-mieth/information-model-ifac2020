# evolution-of-information-model-ifac2020
Source files for the bachelor thesis "Evolution of an Information Model to Manage Dependencies in Interdisciplinary Engineering" authored by Robert Mieth.
Based on the paper "A Knowledge Based System for Managing Heterogeneous Sources of Engineering Information" by Felix Ocker, Birgit Vogel-Heuser, Matthias Seitz, Christiaan J. J. Paredis. This paper has been submitted to the IFAC World Congress 2020. Forked from https://github.com/felixocker/information-model-ifac2020.

# Contents
## knowledge graph creation (OWL)
* filecrawler.py - module that crawls a given path to extract files and their metadata
* informationmodel.py - module that contains classes and instances relevant for the feasibility study
* instancemodel.py - module that generates the populated information model
* integrationpopulated.py - integrates informationmodel.py and instancemodel.py

* manualmod.py - module to manually modify the populated information model
* modifyrelation.py - prototypical function to modify relations within the populated information model on the basis of string input
## queries (SPARQL)
* consistency.py - checks consistency of the knowledge graph created
* findinfo.py - find information based on the type and system described
* duplicateinfo.py - identify duplicate information
* formatcompatibility.py - identify inaccessible information
* changepropagation.py - identify actors affected by a change
* listelements.py - query for listing all classes or instances of a knowledge graph
## auxiliary files
* preprocess.py - module that preprocesses strings for URI/IRI conformity
* importcsv.py - module that imports mappings from .csv files
* executequery.py - module for executing SPARQL queries
* simplegui.py - the name says it all

# Requirements
Python 3.7+ is recommended.

# License
GPL v3.0

# Contact
[robert.mieth@tum.de](mailto:robert.mieth@tum.de)
[felix.ocker@tum.de](mailto:felix.ocker@tum.de)
