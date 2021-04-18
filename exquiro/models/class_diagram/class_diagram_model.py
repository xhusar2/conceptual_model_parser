from ..model import Model
from lxml import etree
from neomodel import StructuredNode, StringProperty, ArrayProperty, Relationship, config, StructuredRel, JSONProperty, \
    UniqueIdProperty


class ClsDiagramModel(Model):

    def __init__(self, model_id, classes, associations, association_nodes, association_classes,
                 association_class_connections, generalizations, generalization_sets, c_types, a_types,
                 enumerations, *model_metadata):
        self.id = model_id
        self.classes = classes
        self.associations = associations
        self.association_nodes = association_nodes
        self.generalizations = generalizations
        self.generalization_sets = generalization_sets
        self.class_types = c_types
        self.association_types = a_types
        self.association_classes = association_classes
        self.association_class_connections = association_class_connections
        self.enumerations = enumerations
        self.model_metadata = model_metadata

    def get_classes(self):
        return self.classes

    def get_associations(self):
        return self.associations

    def get_association_nodes(self):
        return self.association_nodes

    def get_association_classes(self):
        return self.association_classes

    def get_generalizations(self):
        return self.generalizations

    def get_gsets(self):
        return self.generalization_sets

    def get_types(self):
        return self.class_types, self.association_types

    def get_enumerations(self):
        return self.enumerations

    def get_namespaces(self):
        return etree.parse(self.model_file).getroot().nsmap

    def get_neo4j_model(self):
        nodes = {}
        relations = []
        for c in self.classes:
            if c.id in self.class_types:
                class_type = self.class_types[c.id]
            else:
                class_type = ""
            node = Class(_id=c.id, name=c.name, type=class_type, model_id=self.id, model_metadata=self.model_metadata)
            nodes[node._id] = node
            for a in c.attributes:
                attrib = Attribute(_id=a.id, name=a.name, model_id=self.id, model_metadata=self.model_metadata)
                nodes[attrib._id] = attrib
                # relation
                rel_source = node._id
                rel_dest = attrib._id
                rel_props = {}
                rel_attrib = "attribute"
                relations.append((rel_source, rel_dest, rel_props, rel_attrib))

        for n in self.association_nodes:
            node = AssociationNode(model_id=self.id, _id=n.node_id, model_metadata=self.model_metadata)
            nodes[node._id] = node
        for c in self.generalization_sets:
            node = GeneralizationSet(_id=c.id, name=c.name, attributes=[str(a) for a in c.attributes],
                                     model_id=self.id, model_metadata=self.model_metadata)
            nodes[node._id] = node

        for e in self.enumerations:
            node = Enumeration(_id=e.id, name=e.name, values=[str(a) for a in e.values],
                               model_id=self.id, model_metadata=self.model_metadata)
            nodes[node._id] = node

        for association in self.associations:
            if association.src in nodes and association.dest in nodes:
                rel_source = association.src
                rel_dest = association.dest
                rel_props = {
                    'association_type': self.association_types[
                        association.id] if association.id in self.association_types else "",
                    'src_properties': association.src_props,
                    'dest_properties': association.dest_props,
                    'src_cardinality_lower_val': association.src_cardinality_lower_val,
                    'src_cardinality_upper_val': association.src_cardinality_upper_val,
                    'dest_cardinality_lower_val': association.dest_cardinality_lower_val,
                    'rel.dest_cardinality_upper_val': association.dest_cardinality_upper_val
                }
                rel_attrib = 'association'
                relations.append((rel_source, rel_dest, rel_props, rel_attrib))

        for ac in self.association_classes:
            node = AssociationClass(model_id=self.id, _id=ac.node_id, model_metadata=self.model_metadata)
            nodes[node._id] = node

        for acc in self.association_class_connections:
            if acc.src in nodes and acc.dest in nodes:
                rel_source = acc.src
                rel_dest = acc.dest
                rel_attrib = 'association_class_connection'
                relations.append((rel_source, rel_dest, {}, rel_attrib))

        for generalization in self.generalizations:
            if generalization.dest is not None and generalization.src is not None:
                rel_source = generalization.dest
                rel_dest = generalization.src
                rel_props = {
                    '_type': generalization.relation_type,
                    'src_properties': [],
                    'dest_properties': [],
                    'generalization_id': generalization.id
                }
                rel_attrib = 'generalization'
                relations.append((rel_source, rel_dest, rel_props, rel_attrib))

        return nodes, relations


class BaseNode(StructuredNode):
    model_metadata = JSONProperty()


class BaseRelation(StructuredRel):
    model_metadata = JSONProperty()


class GeneralizationRel(BaseNode):
    generalization_id = StringProperty()
    _type = StringProperty()
    src_properties = JSONProperty()
    dest_properties = JSONProperty()


class AssociationRel(BaseRelation):
    _id = StringProperty()
    relation_type = "Association"
    association_type = StringProperty()
    src_cardinality_lower_val = StringProperty()
    src_cardinality_upper_val = StringProperty()
    dest_cardinality_lower_val = StringProperty()
    dest_cardinality_upper_val = StringProperty()
    src_properties = JSONProperty()
    dest_properties = JSONProperty()


class GeneralizationSet(BaseNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    attributes = ArrayProperty()


class Enumeration(BaseNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    values = ArrayProperty()


class Attribute(BaseNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    attrib_type = StringProperty()


class AssociationNode(BaseNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    association = Relationship("Class", "association", model=AssociationRel)


class Class(BaseNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    type = StringProperty()
    generalization = Relationship("Class", "generalization", model=GeneralizationRel)
    association = Relationship("Class", "association", model=AssociationRel)
    attribute = Relationship("Attribute", "has")


class AssociationClass(BaseNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    name = StringProperty()
    type = StringProperty()
    association_class_connection = Relationship("Class", "connects")
