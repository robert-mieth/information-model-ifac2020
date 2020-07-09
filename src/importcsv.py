#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Imports mappings from .csv"""
import types
import csv

def imp_form_comp():
    """Imports the tool - file format compatibility mapping from a .csv"""
    results = []
    with open('ImportFormatCompatibility.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            results.append(row)
    return results

def imp_file_ass():
    """Imports the file extension-information type/role mapping from a .csv"""
    results = []
    with open('ImportFileAssertion.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            results.append(row)
    return results