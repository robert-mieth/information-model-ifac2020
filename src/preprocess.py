#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""module to preprocess query results, and strings for URI conformity"""

def pp(li):
    newlist=[]
    for i in li:
        tempelement = str(i[0])
        templist = tempelement.split(".",1)
        newlist.append(":"+templist[-1])
    return newlist

def pp_str(some_string):
    """replaces whitespaces, umlauts, non URI-conform characters in file paths/names"""
    some_string = str(some_string)
    new_string = some_string
    new_string = new_string.replace(" ","_")
    new_string = new_string.replace("ä","ae")
    new_string = new_string.replace("Ä","Ae")
    new_string = new_string.replace("ö","oe")
    new_string = new_string.replace("Ö","Oe")
    new_string = new_string.replace("ü","ue")
    new_string = new_string.replace("Ü","Ue")
    # Percent encoding of reserved URI characters
    if "%" in some_string:
        new_string = some_string.replace("%","%25")
    new_string = new_string.replace("!","%21")
    new_string = new_string.replace("#","%23")
    new_string = new_string.replace("$","%24")
    new_string = new_string.replace("&","%26")
    new_string = new_string.replace("'","%27")
    new_string = new_string.replace("(","%28")
    new_string = new_string.replace(")","%29")
    new_string = new_string.replace("*","%2A")
    new_string = new_string.replace("+","%2B")
    new_string = new_string.replace(",","%2C")
    new_string = new_string.replace("/","%2F")
    new_string = new_string.replace(":","%3A")
    new_string = new_string.replace(";","%3B")
    new_string = new_string.replace("=","%3D")
    new_string = new_string.replace("?","%3F")
    new_string = new_string.replace("@","%40")
    new_string = new_string.replace("[","%5B")
    new_string = new_string.replace("]","%5D")
    return new_string
