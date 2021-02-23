from ..Model import Model
from lxml import etree
from neomodel import StructuredNode, StringProperty, ArrayProperty, Relationship, config, StructuredRel, JSONProperty,\
    UniqueIdProperty


class PackageDiagramModel(Model):

    def __init__(self, model_id, nodes, relations):
        self.id = model_id
        self.nodes = nodes
        self.relations = relations

    # return dict id, node
    def get_neo4j_model(self):
        m_nodes = {}
        relations = []

        for n in self.nodes:
            if n.node_class == "Package":
                node = Package(_id=n.id, name=n.name, type=n.node_class, model_id=self.id, visibility=n.visibility)
            else:
                node = None
            m_nodes[node._id] = node

        for r in self.relations:
            if r.dest is not None and r.src is not None:
                rel_source = r.dest
                rel_dest = r.src
                rel_props = {
                    'rel_type': r.relation_type,
                    'relation_id': r.id,
                }
                rel_attrib = r.relation_type
                relations.append((rel_source, rel_dest, rel_props, rel_attrib))

        return m_nodes, relations


class RelationModel(StructuredRel):
    relation_id = StringProperty()
    rel_type = StringProperty()


class Package(StructuredNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    type = StringProperty()
    visibility = StringProperty()
    Dependency = Relationship("Package", "dependency", model=RelationModel)
    PackageMerge = Relationship("Package", "merge", model=RelationModel)
    PackageImport = Relationship("Package", "import", model=RelationModel)
    MemberOf = Relationship("Package", "memberOf", model=RelationModel)
