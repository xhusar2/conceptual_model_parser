from lxml import etree
from models.classDiagram.Node import Node
from models.classDiagram.Association import Association
from models.classDiagram.Generalization import Generalization
from models.classDiagram.Attribute import Attribute
from models.classDiagram.GeneralizationSet import GeneralizationSet
import re


class Model:

    def __init__(self, model_file):
        self.id = ""
        self.classes = []
        self.associations = []
        self.generalizations = []
        self.generalization_sets = []
        self.association_nodes = []
        self.class_types = {}
        self.association_types = {}
        self.model_file = model_file
        self.namespaces = self.get_namespaces()
        self.model = self.get_model()

    def get_classes(self):
        return self.classes

    def get_associations(self):
        return self.associations

    def get_association_nodes(self):
        return self.association_nodes

    def get_generalizations(self):
        return self.generalizations

    def get_gsets(self):
        return self.generalization_sets

    def get_types(self):
        return self.class_types, self.association_types

    def get_namespaces(self):
        return etree.parse(self.model_file).getroot().nsmap

    # TODO xml verification
    # def get_xml_schema(self):
    #    with  open("./xmlSchemas/xsd_20071001.xsd", "r") as f:
    #        xmlschema_doc = etree.parse(f)
    #        return etree.XMLSchema(xmlschema_doc)

    # parses association and class types
    # implement in format specific model class
    def parse_types(self, format_class):
        pass

    def parse_generalization_sets(self):
        gsets = self.model.findall('.//packagedElement[@xmi:type="uml:GeneralizationSet"]', self.namespaces)
        for g in gsets:
            self.parse_gset(g)
        return self.generalization_sets

    def parse_gset(self, gs):
        gs_id = gs.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = gs.attrib["name"]
        attributes = {}
        attributes['complete'] = bool(gs.attrib["isCovering"])
        attributes['disjoint'] = bool(gs.attrib["isDisjoint"])
        generalizations = gs.findall('./generalization', self.namespaces)
        attributes['generalizations'] = []
        for g in generalizations:
            g_id = g.attrib["{" + self.namespaces['xmi'] + "}" + "idref"]
            attributes['generalizations'].append(g_id)

        gset = GeneralizationSet(name, gs_id, attributes)
        self.generalization_sets.append(gset)

    def parse_classes(self):
        classes = self.model.findall('.//packagedElement[@xmi:type="uml:Class"]', self.namespaces)
        for c in classes:
            self.parse_class(c)

    def parse_class(self, c):
        parsed_attributes = self.parse_attributes(c)
        # new node
        node_id = c.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        n = Node(c.attrib["name"], node_id, "uml:Class", parsed_attributes)
        # print(n)
        self.classes.append(n)
        # parse sub classes, if present
        nestedClassifiers = c.findall('nestedClassifier', namespaces=self.namespaces)
        for nc in nestedClassifiers:
            if "{" + self.namespaces['xmi'] + "}type" in nc.attrib and nc.attrib[
                "{" + self.namespaces['xmi'] + "}type"] == "uml:Class":
                self.parse_class(nc)
        # parse generalization, if present
        generalization = c.find('generalization', namespaces=self.namespaces)
        if generalization is not None:
            self.parse_generalization(generalization, node_id)

    def parse_attributes(self, c):
        result = []
        attributes = c.findall('ownedAttribute', self.namespaces)
        for a in attributes:
            # attrib_id, value = self.parse_attribute(a)
            # result[attrib_id] = value
            result.append(self.parse_attribute(a))
        return result

    def parse_association(self, a):
        # parses association based on specific model format, implemented in format specific model class
        pass

    def parse_owned_ends(self, a):
        # parses association based on specific model format, implemented in format specific model class
        pass

    def parse_model(self):
        self.get_model_id()
        self.parse_classes()
        self.parse_associations()
        self.parse_generalization_sets()
        self.parse_types()

    def parse_generalization(self, generalization, node_id):
        generalization_id = generalization.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = "Generalization"
        src = generalization.attrib["general"]
        dest = node_id
        r = Generalization(generalization_id, name, src, dest)
        self.generalizations.append(r)
        return r

    def parse_attribute(self, attribute):
        attrib_id = attribute.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = ""
        if "name" in attribute.attrib:
            name = attribute.attrib["name"]
        a = Attribute(attrib_id, name)
        return a

    def get_model(self):
        return etree.parse(self.model_file).find('uml:Model', self.namespaces)

    def parse_associations(self):
        # find model
        model = self.get_model()
        associations = model.findall('.//packagedElement[@xmi:type="uml:Association"]', self.namespaces)
        for a in associations:
            self.parse_association(a)

    def find_ref_element(self, model, id_ref):
        pass
