#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Instantiates the FILES detected by the filecrawler"""

from owlready2 import get_ontology
from owlready2 import Thing
from owlready2 import ObjectProperty
from owlready2 import DataProperty
from owlready2 import IRIS
from collections import Counter
from itertools import tee, count
import types
import datetime
import preprocess

METAFILE = "information-model.owl"
ONTOFILE = "empty-instance-model.owl"
FILES = []

def instancemodel_population(iri, output):
    """definition of information instance model"""
    onto = get_ontology(iri).load()
    with onto:
        #classes
        class folder(Thing): pass
        class new_doc_format(onto.doc_format):
            comment = ["contains doc_formats, which are detected by crawling, that are not contained in the information model"]
        # object properties
        class has_filesize(DataProperty):
            range = [int]
        class has_path(DataProperty):
            range = [str]
        class is_in_folder(ObjectProperty): pass
        # reusable individuals: Examples and relations added to enable testing of queries without manual modification
        ## languages
        ## views
        ## tools
        ## formats - omit
        ## tool support
        ## refinements
        ## individuals - organization
        TUM = onto.university("TUM")
        Robert = onto.person("Robert")
        ## organizational licenses
        TUM.has_license_for.extend([onto.CODESYS,onto.Eclipse,onto.VS_Code,onto.TwinCAT_3]) #onto.AutoCAD_2021,onto.Inventor_2021,
        ## PPU structure
        Crane = onto.system("Crane")
        ## PPU info
        ## information concretizations - omit
        CraneDrawing = onto.information_concretization("CraneDrawing")
        ## information carriers - omit
        Drive1 = onto.information_carrier("Drive1")
        ## information carrier relations - omit
        ## PPU relations
        ## relations between information concretizations and actors
        onto.CraneDrawing.stored_as.append(IRIS["http://david.org/informationmodel.owl#" + ".dwg"])
        onto.CraneDrawing.describes.append(onto.Crane)
        onto.Robert.subscribes.append(onto.CraneDrawing)
        onto.Drive1.captures.append(CraneDrawing)

        # create unique names for ICs to distinguish identically named copies of files
        list_file_names = []
        unique_FILES = FILES
        for i in range(0, len(FILES)):
            list_file_names.append(FILES[i][0])
        uniquify(list_file_names, (f'_{x!s}' for x in range(1, 600)))
        for i in range(0, len(FILES)):
            unique_FILES[i][0] = list_file_names[i]

        # instance and object/data property generation: processing of file crawler results FILES
        file_names = list(onto.information_concretization.instances())
        info_carriers = list(onto.information_carrier.instances())
        doc_format_list = list(onto.doc_format.instances())
        folders = list(onto.folder.instances())

        for i in range(0, len(FILES)):
            
            # IC creation and annotations
            file_name = str(unique_FILES[i][0])
            file_name = preprocess.pp_str(file_name)
            iri_file_name = IRIS["http://david.org/informationmodel.owl#" + file_name]
            if iri_file_name not in file_names:
                file_name = onto.information_concretization(file_name)
                file_name.comment = [str(FILES[i][0])]
                file_name.comment.append("extension: " + str(FILES[i][1]))
                file_name.comment.append("size (bytes): " + str(FILES[i][2]))
                file_name.comment.append("timestamp modification: " + str(FILES[i][3]))
                file_name.comment.append("timestamp creation: " + str(FILES[i][4]))
                file_name.comment.append("timestamp access: " + str(FILES[i][5]))
                file_name.comment.append("path: " +  '"' + str(FILES[i][6]) + '"')
                iri_file_name = file_name
                print("Information concretization " + str(iri_file_name) + " added")
            if not (iri_file_name.has_filesize == [FILES[i][2]]):
                iri_file_name.has_filesize = [FILES[i][2]]
                print(str(iri_file_name) + " has_filesize " + str(FILES[i][2]) + " added")

            # information concretization timestamps
            try:
                dt_mod = iri_file_name.timestamp_modification[0]
                dt_cr = iri_file_name.timestamp_creation[0]
                dt_ac = iri_file_name.timestamp_access[0]
            except:
                dt_mod = iri_file_name.timestamp_modification
                dt_cr = iri_file_name.timestamp_creation
                dt_ac = iri_file_name.timestamp_access

            datetime_temp = datetime.datetime.fromtimestamp(FILES[i][3])
            datetime_temp = datetime_temp.replace(microsecond=0)
            if not (dt_mod == datetime_temp):
                iri_file_name.timestamp_modification = [datetime_temp]
                print(str(iri_file_name) + " timestamp_modification " + str(datetime_temp) + " added")

            datetime_temp = datetime.datetime.fromtimestamp(FILES[i][4])
            datetime_temp = datetime_temp.replace(microsecond=0)
            if not ( dt_cr == datetime_temp):
                iri_file_name.timestamp_creation = [datetime_temp]
                print(str(iri_file_name) + " timestamp_creation " + str(datetime_temp) + " added")

            datetime_temp = datetime.datetime.fromtimestamp(FILES[i][5])
            datetime_temp = datetime_temp.replace(microsecond=0)
            if not ( dt_ac == datetime_temp):
                iri_file_name.timestamp_access = [datetime_temp]
                print(str(iri_file_name) + " timestamp_access " + str(datetime_temp) + " added")

            # filepath and information carrier
            if not (iri_file_name.has_path == [FILES[i][6]]):
                iri_file_name.has_path = [FILES[i][6]]
                print(str(iri_file_name) + " has_path " + str(FILES[i][6]) + " added")
            info_carrier_name = str(FILES[i][6])
            info_carrier_name = preprocess.pp_str(info_carrier_name)
            info_carrier_name = info_carrier_name[0]
            iri_info_carrier = IRIS["http://david.org/informationmodel.owl#" + info_carrier_name]
            if iri_info_carrier not in info_carriers:
                info_carrier_name = onto.information_carrier(info_carrier_name)
                iri_info_carrier = info_carrier_name
                print("Information carrier " + str(iri_info_carrier) + " added")
            if (iri_file_name not in file_names):
                iri_info_carrier.captures.append(iri_file_name)
                print(str(iri_info_carrier) + " captures " + str(iri_file_name) + " added")

            # formats
            new_format = str(FILES[i][1])
            new_format = preprocess.pp_str(new_format)
            iri_new_format = IRIS["http://david.org/informationmodel.owl#" + new_format]
            if (iri_new_format in doc_format_list):
                iri_file_name.stored_as = [iri_new_format]
                if iri_file_name not in file_names:
                    print(str(iri_file_name) + " stored_as " + str(iri_new_format) + " added")
                    pass
            else:
                new_format = onto.new_doc_format(new_format)
                iri_new_format = new_format
                print("Format " + str(new_format) + " added")
                iri_file_name.stored_as = [new_format]
                print(str(iri_file_name) + " stored_as " + str(new_format) + " added")

            # containing folders (omits printing all containing folders of a single file, as they are elements of path)
            for j in range(1,(len(FILES[i][7])-1)):
                folder_name = str(FILES[i][7][j])
                folder_name = preprocess.pp_str(folder_name)
                iri_folder = IRIS["http://david.org/informationmodel.owl#" + str(folder_name)]
                if iri_folder not in folders:
                    folder_name = folder(folder_name)
                    iri_folder = folder_name
                    print("Folder " + str(folder_name) + " added")
                if (iri_file_name not in file_names):
                    iri_file_name.is_in_folder.append(iri_folder)
            
            # append new instances
            if (iri_file_name not in file_names):
                file_names.append(iri_file_name)
            if (iri_info_carrier not in info_carriers):    
                info_carriers.append(iri_info_carrier)
            if (iri_new_format not in doc_format_list):    
                doc_format_list.append(iri_new_format)
            if (iri_folder not in folders):    
                folders.append(iri_folder)
                
    onto.save(file=output)

def verify_existence(iri):
    # Verifies existence of ICs' original names in file crawler results FILES
    onto = get_ontology(iri).load()
    with onto:
        ic_names = list(onto.information_concretization.instances())
        for i in range(1,len(ic_names)):
            ic_name = ic_names[i]
            try:
                orig_file_name = ic_name.comment[0]
                orig_file_path = ic_name.comment[6]
            except:
                orig_file_name = ic_name.comment
            files = []
            for j in range(0,len(FILES)):
                files.append(str(FILES[j][0]))
            if orig_file_name and (str(orig_file_name) not in files):
                print(str(orig_file_name) + " existence could not be verified by filecrawling. Check " + str(orig_file_path))

def uniquify(seq, suffs = count(1)):
    """Make all the items unique by adding a suffix (1, 2, etc).
    `seq` is mutable sequence of strings.
    `suffs` is an optional alternative suffix iterable.
    """
    # Copy from https://stackoverflow.com/questions/30650474/python-rename-duplicates-in-list-with-progressive-numbers-without-sorting-list
    not_unique = [k for k,v in Counter(seq).items() if v>1]
    # suffix generator dict - e.g., {'name': <my_gen>, 'zip': <my_gen>}
    suff_gens = dict(zip(not_unique, tee(suffs, len(not_unique))))
    for idx,s in enumerate(seq):
        try:
            suffix = str(next(suff_gens[s]))
        except KeyError:
            # s was unique
            continue
        else:
            seq[idx] += suffix


def main():
    instancemodel_population(METAFILE,ONTOFILE)


if __name__ == "__main__":
    main()