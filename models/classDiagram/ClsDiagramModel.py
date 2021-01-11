from lxml import etree
from models.classDiagram.Node import Node
from models.classDiagram.Association import Association
from models.classDiagram.Generalization import Generalization
from models.classDiagram.Attribute import Attribute
from models.classDiagram.GeneralizationSet import GeneralizationSet
import re


class ClsDiagramModel:
    #delete
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

    def __init__(self, model_id, classes, associations, association_nodes, generalizations, generalization_sets, c_types, a_types):
        self.id = model_id
        self.classes = classes
        self.associations = associations
        self.association_nodes = association_nodes
        self.generalizations = generalizations
        self.generalization_sets = generalization_sets
        self.class_types = c_types
        self.association_types = a_types

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

