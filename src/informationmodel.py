#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Creates a generic information model"""

import types
from owlready2 import datetime
from owlready2 import get_ontology
from owlready2 import Thing
from owlready2 import ObjectProperty
from owlready2 import DataProperty
from owlready2 import TransitiveProperty
from owlready2 import Inverse
import importcsv
import preprocess

IRI = "http://david.org/informationmodel.owl"
METAFILE = "empty-information-model.owl"

def im_informationmodel(iri, output):
    """Generates a generic information model"""
    fileassertion = importcsv.imp_file_ass()
    formatcompatibility = importcsv.imp_form_comp()
    onto = get_ontology(iri)
    with onto:
    # universals
        class actor(Thing):
            comment = ["anyone and anything that provides or requires information"]
        class doc_format(Thing):
            comment= ["concrete syntax some information concretization is stored in; e.g. plain text or pdf; indicates the information concretizations's structure and how it has to be interpreted"]
            comment.append("Reserved URI characters are percent encoded in the form '%XX' ")
        class event(Thing): pass
        class information(Thing):
            comment = ["the communication or reception of knowledge [Merriam-Webster]"]
        class information_carrier(Thing):
            comment = ["physical artifact that captures some information concretization"]
        class information_concretization(Thing):
            comment = ["concretization of some information, i.e., some information being ex- pressed in some language and possibly serialized in some format"]
            comment.append("an information concretization refers to the combination of information expressed in at least one specific language. combinations of languages may be necessary, e.g., UML and English")
        class language(Thing):
            comment = ["set of valid sentences that can be used to express information"]
        class organization(Thing): pass
        class organizational_unit(Thing): pass
        class project(Thing):
            comment = ["an endeavor with start and finish dates undertaken to create a product or service in accordance with specified resources and requirements [INCOSE SE Handbook]"]
        class role(Thing):
            comment = ["concept of the extended information model; further characterizes information; taken on by a specific doc_format"]
        class system(Thing):
            comment = ["a combination of interacting elements organized to achieve one more stated purposes [INCOSE SE Handbook]"]
        class task(Thing): pass
        class viewpoint(Thing): pass
    # dependent universals
        class behavioral_information(information):
            comment = ["defines the behavior of a system"]
        class requirement(information):
            comment = ["condition or capability that must be possessed by a system or system component to satisfy a contract, standard, specification, or other formally imposed information carriers (IEEE glossary)"]
        class structural_information(information):
            comment = ["defines the structure of a system"]
        class function(behavioral_information): pass
        class company(organization): pass
        class discipline(viewpoint): pass
        class functional_requirement(requirement):
            comment = ["requirement that specifies a function that a system or system component must be able to perform (IEEE glossary)"]
        class non_functional_requirement(requirement):
            comment = ["opposed to functional requirements, a non-functional requirement specifies (IEEE glossary)"]
        class person(actor): pass
        class tool(actor): pass
        class university(organization): pass
    # object properties
        class authored_by(information_concretization >> actor):
            comment = ["every information-concretization has some author, some information-concretizations, e.g., books, may have several authors"]
        class based_on(doc_format >> doc_format): pass
        class can_format(information_concretization >> information): pass
        class can_perform(system >> function): pass
        class captures(information_carrier >> information_concretization):
            comment = ["an information carrier may capture several information concretizations"]
        class concretizes(information_concretization >> information):
            comment = ["an information concretization concretizes information"]
        class defines(project >> requirement): pass
        class describes(ObjectProperty): pass
        class expressed_in(information_concretization >> language):
            comment = ["an information concretization is expressed in at least one language, e.g., UML and English might be used together"]
        class has(ObjectProperty): pass
        class has_license_for(organization >> tool): pass
        class has_right(ObjectProperty): pass
        class has_role(doc_format >> role): pass
        class part(Thing >> Thing, TransitiveProperty): pass
        class performs(system >> function): pass
        class possesses(person >> information): pass
        class has_predecessor(information_concretization >> information_concretization):
            comment = ["predecessor relation between information concretizations for versioning "]
        class related_to(information_concretization >> information_concretization):
            comment = ["links dependent ICs to each other for change management"]
        class provides(actor >> information): pass
        class publishes(actor >> information_concretization): pass
        class requires(actor >> information): pass
        class restricts(non_functional_requirement >> system): pass
        class satisfies(system >> requirement): pass
        class specifies(functional_requirement >> function): pass
        class stored_as(information_concretization >> doc_format): pass
        class subscribes(actor >> information_concretization): pass
        class supports(tool >> doc_format): pass
    # dependent object properties
        # currently omitted as not used
        #class has_read_right(has_right): pass
        #class has_write_right(has_right): pass
        #class has_execute_right(has_right): pass
        class submitted_by(authored_by):
            comment = ["every document is submitted by a corresponding author, of which there is exactly one per information concretization"]
    # datatype properties
        class status_complete(DataProperty):
            domain = [information_concretization]
            range = [bool]
            comment = ["status of a information carrier: either complete or incomplete"]
            # todo: consider changing this to an enum
        class timestamp_access(DataProperty):
            domain = [information_concretization]
            range = [datetime.datetime]
            comment = ["date of the last access of an information concretization"]
        class timestamp_creation(DataProperty):
            domain = [information_concretization]
            range = [datetime.datetime]
            comment = ["date of the creation of an information concretization"]
        class timestamp_modification(DataProperty):
            domain = [information_concretization]
            range = [datetime.datetime]
            comment = ["date of the last modification of an information concretization"]
    # axioms - added down here to make sure that all classes are already defined
        actor.is_a.append(has.some(viewpoint))
        doc_format.is_a.append(has_role.some(role))
        doc_format.is_a.append(can_format.some(information))
        functional_requirement.is_a.append(specifies.some(function))
        information.is_a.append(describes.some(system))
        information.is_a.append(has_role.some(role))
        information_carrier.is_a.append(captures.some(information_concretization))
        information_concretization.is_a.append(concretizes.some(information))
        information_concretization.is_a.append(expressed_in.min(1, language))
        information_concretization.is_a.append(stored_as.exactly(1, doc_format))
        information_concretization.is_a.append(authored_by.some(actor))
        information_concretization.is_a.append(submitted_by.exactly(1, actor))
        information_concretization.is_a.append(status_complete.some(bool))
        information_concretization.is_a.append(timestamp_access.some(datetime.datetime))
        information_concretization.is_a.append(timestamp_creation.some(datetime.datetime))
        information_concretization.is_a.append(timestamp_modification.some(datetime.datetime))
        non_functional_requirement.is_a.append(restricts.some(system))
        organizational_unit.is_a.append(Inverse(part).some(organization))
        project.is_a.append(defines.some(requirement))
        system.is_a.append(performs.some(function))

    # instances - generic instances and relations
        some_structural_information = structural_information("some_structural_information")
        some_behavioral_information = behavioral_information("some_behavioral_information")
        prescriptive_role = role("prescriptive_role")
        predictive_role = role("predictive_role")
        descriptive_role = role("descriptive_role")
        diagnostic_role = role("diagnostic_role")

    # file format - information type assertion based on ImportFileAssertion
    # maps the file extension to a probable type of information/role
        for i in range(2, len(fileassertion)):
            file_extension = str(fileassertion[i][1])
            file_extension = preprocess.pp_str(file_extension)
            file_extension = onto.doc_format(file_extension)
            if fileassertion[i][3] != "":
                file_extension.can_format.append(some_structural_information)
            if fileassertion[i][4] != "":
                file_extension.can_format.append(some_behavioral_information)
            if fileassertion[i][5] != "":
                file_extension.has_role.append(prescriptive_role)
            if fileassertion[i][6] != "":
                file_extension.has_role.append(predictive_role)
            if fileassertion[i][7] != "":
                file_extension.has_role.append(descriptive_role)
            if fileassertion[i][8] != "":
                file_extension.has_role.append(diagnostic_role)
    # tools and the file can_format they support - based on formatcompatibility
        for i in range(1, len(formatcompatibility)):
            tool_name = str(formatcompatibility[i][2])
            tool_name = preprocess.pp_str(tool_name)
            tool_name = tool(tool_name)
            if (formatcompatibility[i][5] and formatcompatibility[i][6]):
                file_extension = str(formatcompatibility[i][3])
                file_extension = preprocess.pp_str(file_extension)
                file_extension = doc_format(file_extension)
                tool_name.supports.append(file_extension)
    # save file
    onto.save(file = output)


def main():
    im_informationmodel(IRI,METAFILE)


if __name__ == "__main__":
    main()