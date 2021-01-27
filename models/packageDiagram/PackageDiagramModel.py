from ..Model import Model
from lxml import etree
from neomodel import StructuredNode, StringProperty, ArrayProperty, Relationship, config, StructuredRel, JSONProperty,\
    UniqueIdProperty


class PackageDiagramModel(Model):

    def __init__(self, model_id, classes, associations):
        self.id = model_id
        self.classes = classes
        self.associations = associations

