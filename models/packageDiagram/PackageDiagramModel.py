from ..Model import Model
from neomodel import StructuredNode, StringProperty, Relationship, StructuredRel, UniqueIdProperty


class PackageDiagramModel(Model):

    def __init__(self, model_id, nodes, relations):
        self.id = model_id
        self.nodes = nodes
        self.relations = relations

    def get_neo4j_model(self):
        m_nodes = {}
        relations = []

        for n in self.nodes:
            if n.node_type == "Package":
                node = Package(_id=n.id, name=n.name, node_type=n.node_type, model_id=self.id, visibility=n.visibility)
            else:
                node = None
            if node is not None:
                m_nodes[n.id] = node

        for r in self.relations:
            if r.target is not None and r.source is not None:
                rel_source = r.source
                rel_dest = r.target
                rel_props = {
                    'rel_type': r.relation_type,
                    'relation_id': r.id,
                    'model_id': self.id
                }
                rel_attrib = r.relation_type
                relations.append((rel_source, rel_dest, rel_props, rel_attrib))

        return m_nodes, relations


class RelationModel(StructuredRel):
    relation_id = StringProperty()
    rel_type = StringProperty()
    model_id = StringProperty()


class Package(StructuredNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    node_type = StringProperty()
    visibility = StringProperty()
    Dependency = Relationship("Package", "dependency", model=RelationModel)
    PackageMerge = Relationship("Package", "merge", model=RelationModel)
    PackageImport = Relationship("Package", "import", model=RelationModel)
    MemberOf = Relationship("Package", "memberOf", model=RelationModel)
    Usage = Relationship("Package", "use", model=RelationModel)
    PackageAccess = Relationship("Package", "access", model=RelationModel)
