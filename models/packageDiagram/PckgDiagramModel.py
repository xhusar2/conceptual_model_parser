from ..Model import Model
from lxml import etree
from neomodel import StructuredNode, StringProperty, ArrayProperty, Relationship, config, StructuredRel, JSONProperty,\
    UniqueIdProperty


class PackageDiagramModel(Model):

    def __init__(self, model_id, packages, relations):
        self.id = model_id
        self.packages = packages
        self.relations = relations

    # return dict id, node
    # TODO ofuskovane package must have attribute e.x. dependency
    def get_neo4j_model(self):
        nodes = {}
        relations = []

        for p in self.packages:
            node = Package(_id=p.id, name=p.name, type="Package", model_id=self.id)
            nodes[node._id] = node

        for r in self.relations:
            relations.append((r.src, r.dest, r.id, r.relation_type))

        return nodes, relations


class Package(StructuredNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    type = StringProperty()

