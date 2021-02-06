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
            if r.dest is not None and r.src is not None:
                rel_source = r.dest
                rel_dest = r.src
                rel_props = {
                    '_type': r.relation_type,
                    'src_properties': [],
                    'dest_properties': [],
                    'dependency_id': r.id
                }
                rel_attrib = 'dependency'
                relations.append((rel_source, rel_dest, rel_props, rel_attrib))

        return nodes, relations


class DependencyRel(StructuredRel):
    dependency_id = StringProperty()
    _type = StringProperty()
    src_properties = JSONProperty()
    dest_properties = JSONProperty()


class Package(StructuredNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    type = StringProperty()
    dependency = Relationship("Package", "dependency", model=DependencyRel)
