#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""simple gui for interaction with the information model"""

###########################################################
# FIXME duplicate info: excessive runtime + GUI freeze
###########################################################


import datetime
from contextlib import redirect_stdout
from io import StringIO
import sys
import tkinter as tk
from tkinter import ttk
import changepropagation
import consistency
import duplicateinfo
import findinfo
import formatcompatibility
import listelements
import manualmod
import modifyrelation
from preprocess import pp

class exit_button(tk.Button):
    def __init__(self, master):
        tk.Button.__init__(self, master, text="Exit",  command=window.quit)

def call_external(ext, content, lbl):
    funcs = {'consistency': consistency.main,
             'duplicate': duplicateinfo.main,
             'format': formatcompatibility.main}
    labels = {'consistency': "Consistency check executed!",
              'duplicate': "Check for information duplicates executed!",
              'format': "Format compatibility check executed!"}
    with StringIO() as buf, redirect_stdout(buf):
        try:
            funcs[ext]()
        except KeyError:
            print('causes an error - unknown function type')
            sys.exit(1)
        content.config(text=buf.getvalue())
    lbl.config(text=labels[ext])

def call_change(content, lbl, infoconc):
    with StringIO() as buf, redirect_stdout(buf):
        changepropagation.main(infoconc)
        content.config(text=buf.getvalue())
    lbl.config(text="Change propagation check completed!")

def call_find(content, lbl, infokind, role):
    #FIXME GUI freezes and long runtime, if SPARQL query execution is lengthy -> possibly a thread issue
    with StringIO() as buf, redirect_stdout(buf):
        findinfo.returnresult(infokind=infokind,role=role)
        content.config(text=buf.getvalue())
    lbl.config(text="Find info completed!")

def call_insert_relation(content, lbl, instance1, relation, instance2):
    with StringIO() as buf, redirect_stdout(buf):
        manualmod.insert_relation(instance1, relation, instance2)
        content.config(text=buf.getvalue())
    lbl.config(text=str("insert_relation has been called."))

def call_remove_instance(content, lbl, instance):
    with StringIO() as buf, redirect_stdout(buf):
        manualmod.remove_entity(instance)
        content.config(text=buf.getvalue())
    lbl.config(text=str("remove_entity has been called."))

#def call_modify_relation(content, lbl, instance1, relation, instance2, mode):
#    with StringIO() as buf, redirect_stdout(buf):
#        modifyrelation.modify_relation(instance1, relation, instance2, mode)
#        content.config(text=buf.getvalue())
#    lbl.config(text=str("modify_relation has been called."))

# general setup
window = tk.Tk()
window.title("information model")
window.geometry('1440x1080')
window.resizable(width=False, height=False)
window.option_add("*font","arial 10")

s = ttk.Style()
s.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"font" : ('arial', '10', 'bold')} },
        "TNotebook.Tab": {"configure": {"padding": [50, 5],
                                        "font" : ('arial', '10', 'bold')},}})
s.theme_use("MyStyle")

#tabs
tab_parent = ttk.Notebook(window)
tab_consistency = ttk.Frame(tab_parent)
tab_duplicateinfo = ttk.Frame(tab_parent)
tab_formatcompatibility = ttk.Frame(tab_parent)
tab_findinfo = ttk.Frame(tab_parent)
tab_changepropagation = ttk.Frame(tab_parent)
tab_remove_instance = ttk.Frame(tab_parent)
tab_insert_relation = ttk.Frame(tab_parent)
#tab_modify_relation = ttk.Frame(tab_parent)

tab_parent.add(tab_consistency, text="consistency check")
tab_parent.add(tab_duplicateinfo, text="duplicate info")
tab_parent.add(tab_formatcompatibility, text="format compatibility check")
tab_parent.add(tab_findinfo, text="find info")
tab_parent.add(tab_changepropagation, text="check change prop")
tab_parent.add(tab_remove_instance, text="remove entity")
tab_parent.add(tab_insert_relation, text="insert relation")
#tab_parent.add(tab_modify_relation, text="modify relation")
tab_parent.pack(fill="both", expand=True)

# menu
menubar = tk.Menu(window)
file_menu = tk.Menu(menubar, tearoff = 0)
help_menu = tk.Menu(menubar, tearoff = 0)
file_menu.add_command(label="Nothing", command=window.quit)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Help", menu=help_menu)
window.config(menu=menubar)

# tab consistency
consistency_label = tk.Label(tab_consistency, text="Click button to the left to check consistency.")
consistency_output_label = tk.Label(tab_consistency, text="-", anchor="w", justify="left")
exit_button_tab_consistency = exit_button(tab_consistency)
consistency_button = tk.Button(tab_consistency, text="Check consistency", command=lambda: call_external("consistency",consistency_output_label,consistency_label))

consistency_button.grid(row=0, column=0, sticky="w")
consistency_label.grid(row=0, column=1, sticky="w")
consistency_output_label.grid(row=1, column=1, sticky="w")
exit_button_tab_consistency.grid(row=2, column=0, sticky="w")

# tab duplicate info
duplicates_label = tk.Label(tab_duplicateinfo, text="Click button to the left to find duplicate information.")
duplicates_output_label = tk.Label(tab_duplicateinfo, text="-", anchor="w", justify="left")
exit_button_tab_duplicateinfo = exit_button(tab_duplicateinfo)
duplicates_button = tk.Button(tab_duplicateinfo, text="Find duplicate information", command=lambda: call_external("duplicate",duplicates_output_label,duplicates_label))

duplicates_button.grid(row=0, column=0, sticky="w")
duplicates_label.grid(row=0, column=1, sticky="w")
duplicates_output_label.grid(row=1, column=1, sticky="w")
exit_button_tab_duplicateinfo.grid(sticky="w")

# tab format compatibility
format_label = tk.Label(tab_formatcompatibility, text="Click button to the left to find format incompatibilities.")
format_output_label = tk.Label(tab_formatcompatibility, text="-", anchor="w", justify="left")
exit_button_tab_format = exit_button(tab_formatcompatibility)
format_button = tk.Button(tab_formatcompatibility, text="Find format incompatibilities", command=lambda: call_external("format",format_output_label,format_label))

format_button.grid(row=0, column=0, sticky="w")
format_label.grid(row=0, column=1, sticky="w")
format_output_label.grid(row=1, column=1, sticky="w")
exit_button_tab_format.grid(sticky="w")

# tab findinfo
infokind_options = pp(listelements.find_classes(":information"))
infokind = tk.StringVar(tab_findinfo)
infokind.set("choose")
infokind_dropdown = tk.OptionMenu(tab_findinfo, infokind, *infokind_options)
role_options = pp(listelements.find_instances(":role"))
role = tk.StringVar(tab_findinfo)
role.set("choose")
role_dropdown = tk.OptionMenu(tab_findinfo, role, *role_options)

find_label = tk.Label(tab_findinfo, text="Click button to the left to find related information.")
find_output_label = tk.Label(tab_findinfo, text="-", anchor="w", justify="left")
exit_button_tab_find = exit_button(tab_findinfo)
find_button = tk.Button(tab_findinfo, text="Find info", command=lambda: call_find(find_output_label,find_label,
                        infokind=infokind.get(), role=role.get()))

infokind_dropdown.grid(row=0, column=0, sticky="w")
role_dropdown.grid(row=1, column=0, sticky="w")
find_button.grid(row=2, column=0, sticky="w")
find_label.grid(row=2, column=1, sticky="w")
find_output_label.grid(row=3, column=1, sticky="w")
exit_button_tab_find.grid(sticky="w")

# tab change propagation
infoconc_options = pp(listelements.find_instances(":information_concretization"))
infoconc = tk.StringVar(tab_changepropagation)
infoconc.set("choose")
infoconc_dropdown = tk.OptionMenu(tab_changepropagation, infoconc, *infoconc_options)

change_label = tk.Label(tab_changepropagation, text="Click button to the left to check change propagation.")
change_output_label = tk.Label(tab_changepropagation, text="-", anchor="w", justify="left")
exit_button_tab_change = exit_button(tab_changepropagation)
change_button = tk.Button(tab_changepropagation, text="Check change propagation", command=lambda: call_change(change_output_label,change_label,
                        infoconc=infoconc.get()))

infoconc_dropdown.grid(row=0, column=0, sticky="w")
change_button.grid(row=1, column=0, sticky="w")
change_label.grid(row=1, column=1, sticky="w")
change_output_label.grid(row=2, column=1, sticky="w")
exit_button_tab_change.grid(sticky="w")

# tab insert relation
insert_instance1_options = pp(listelements.find_instances("owl:Thing"))
insert_instance1_options = [f[1:] for f in insert_instance1_options]
insert_instance1 = tk.StringVar(tab_insert_relation)
insert_instance1.set("choose")
insert_instance1_dropdown = tk.OptionMenu(tab_insert_relation, insert_instance1, *insert_instance1_options)
insert_instance2_options = insert_instance1_options
insert_instance2 = tk.StringVar(tab_insert_relation)
insert_instance2.set("choose")
insert_instance2_dropdown = tk.OptionMenu(tab_insert_relation, insert_instance2, *insert_instance2_options)
insert_relation_options = list(manualmod.list_relations())
insert_relation = tk.StringVar(tab_insert_relation)
insert_relation.set("choose")
insert_relation_dropdown = tk.OptionMenu(tab_insert_relation, insert_relation, *insert_relation_options)

insert_relation_instance1_label = tk.Label(tab_insert_relation, text="Click button to the left to select instance1.")
insert_relation_instance2_label = tk.Label(tab_insert_relation, text="Click button to the left to select instance2.")
insert_relation_relation_label = tk.Label(tab_insert_relation, text="Click button to the left to select relation.")
insert_relation_label = tk.Label(tab_insert_relation, text="Click button to the left to insert the specified relation.")
insert_output_label = tk.Label(tab_insert_relation, text="-", anchor="w", justify="left")
exit_button_tab_find = exit_button(tab_insert_relation)
insert_relation_button = tk.Button(tab_insert_relation, text="Insert relation", command=lambda: call_insert_relation(insert_output_label,insert_relation_label,
                        instance1=insert_instance1.get(), relation=insert_relation.get(), instance2=insert_instance2.get()))

insert_instance1_dropdown.grid(row=0, column=0, sticky="w")
insert_relation_instance1_label.grid(row=0, column=1, sticky="w")
insert_instance2_dropdown.grid(row=1, column=0, sticky="w")
insert_relation_instance2_label.grid(row=1, column=1, sticky="w")
insert_relation_dropdown.grid(row=2, column=0, sticky="w")
insert_relation_relation_label.grid(row=2, column=1, sticky="w")
insert_relation_button.grid(row=4, column=0, sticky="w")
insert_relation_label.grid(row=4, column=1, sticky="w")
insert_output_label.grid(row=5, column=1, sticky="w")
exit_button_tab_find.grid(sticky="w")

# tab remove instance
remove_instance_options = manualmod.list_instances()
remove_instance = tk.StringVar(tab_remove_instance)
remove_instance.set("choose")
remove_instance_dropdown = tk.OptionMenu(tab_remove_instance, remove_instance, *remove_instance_options)

remove_instance_label = tk.Label(tab_remove_instance, text="Click button to the left to select instance to be removed.")
remove_label = tk.Label(tab_remove_instance, text="Click button to the left to remove the specified instance.")
remove_instance_output_label = tk.Label(tab_remove_instance, text="-", anchor="w", justify="left")
exit_button_tab_find = exit_button(tab_remove_instance)
remove_instance_button = tk.Button(tab_remove_instance, text="Remove instance", command=lambda: call_remove_instance(remove_instance_output_label,remove_instance_label,
                         instance=remove_instance.get()))

remove_instance_dropdown.grid(row=0, column=0, sticky="w")
remove_instance_label.grid(row=0, column=1, sticky="w")
remove_instance_button.grid(row=1, column=0, sticky="w")
remove_instance_output_label.grid(row=1, column=1, sticky="w")
exit_button_tab_find.grid(sticky="w")

# tab modify relation
# instance1_options = pp(listelements.find_instances("owl:Thing"))
# instance1_options = [f[1:] for f in instance1_options]
# instance1 = tk.StringVar(tab_modify_relation)
# instance1.set("choose")
# instance1_dropdown = tk.OptionMenu(tab_modify_relation, instance1, *instance1_options)
# instance2_options = instance1_options
# instance2 = tk.StringVar(tab_modify_relation)
# instance2.set("choose")
# instance2_dropdown = tk.OptionMenu(tab_modify_relation, instance2, *instance2_options)
# relation_options = modifyrelation.list_relations()
# relation = tk.StringVar(tab_modify_relation)
# relation.set("choose")
# relation_dropdown = tk.OptionMenu(tab_modify_relation, relation, *relation_options)
# mode_options = [1,2,3,4]
# mode = tk.IntVar(tab_modify_relation)
# mode.set("choose")
# mode_dropdown = tk.OptionMenu(tab_modify_relation, mode, *mode_options)

# modify_relation_instance1_label = tk.Label(tab_modify_relation, text="Click button to the left to select instance1.")
# modify_relation_instance2_label = tk.Label(tab_modify_relation, text="Click button to the left to select instance2.")
# modify_relation_relation_label = tk.Label(tab_modify_relation, text="Click button to the left to select relation.")
# modify_relation_mode_label = tk.Label(tab_modify_relation, text="Modes: 1: Add object property 2: Remove object property 3: Add data property 4: Remove data property")
# modify_relation_label = tk.Label(tab_modify_relation, text="Click button to the left to modify the specified relation.")
# modify_output_label = tk.Label(tab_modify_relation, text="-", anchor="w", justify="left")
# exit_button_tab_find = exit_button(tab_modify_relation)
# modify_relation_button = tk.Button(tab_modify_relation, text="Modify relation", command=lambda: call_modify_relation(modify_output_label,modify_relation_label,
#                         instance1=instance1.get(), relation=relation.get(), instance2=instance2.get(), mode=mode.get()))

# instance1_dropdown.grid(row=0, column=0, sticky="w")
# modify_relation_instance1_label.grid(row=0, column=1, sticky="w")
# instance2_dropdown.grid(row=1, column=0, sticky="w")
# modify_relation_instance2_label.grid(row=1, column=1, sticky="w")
# relation_dropdown.grid(row=2, column=0, sticky="w")
# modify_relation_relation_label.grid(row=2, column=1, sticky="w")
# mode_dropdown.grid(row=3, column=0, sticky="w")
# modify_relation_mode_label.grid(row=3, column=1, sticky="w")
# modify_relation_button.grid(row=4, column=0, sticky="w")
# modify_relation_label.grid(row=4, column=1, sticky="w")
# find_output_label.grid(row=5, column=1, sticky="w")
# exit_button_tab_find.grid(sticky="w")


window.mainloop()
