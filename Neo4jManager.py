from neomodel import StructuredNode, StringProperty, ArrayProperty, Relationship, config, StructuredRel, JSONProperty,\
    UniqueIdProperty
from neomodel import db as neo_db

# TODO sort out connection and config file
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'


# this class represents Neo4j manager. It stores model to db, deletes models from db, executes queries
class Neo4jManager:

    @staticmethod
    def delete_all():
        neo_db.cypher_query("MATCH ()-[r]-() DETACH DELETE r")
        neo_db.cypher_query("MATCH (n) DETACH DELETE n")

    @staticmethod
    def add_to_db(model):
        nodes = {}
        for n in model.association_nodes:
            node = AssociationNode(model_id=model.id, node_id=n.node_id)
            nodes[n.node_id] = node
            node.save()

        for c in model.classes:
            class_type = ""
            if c.id in model.class_types:
                class_type = model.class_types[c.id]
            node = Class(class_id=c.id, name=c.name, type=class_type, model_id=model.id)
            nodes[c.id] = node
            node.save()
            for a in c.attributes:
                attrib = Attribute(attrib_id=a.id, name=a.name, model_id=model.id)
                attrib.save()
                node.attribute.connect(attrib)

        for c in model.generalization_sets:
            node = GeneralizationSet(gs_id=c.id, name=c.name, attributes=[str(a) for a in c.attributes],
                                     model_id=model.id)
            nodes[c.id] = node
            node.save()

        for association in model.associations:
            if association.src in nodes and association.dest in nodes:
                # rel1 = nodes[r.dest].association.connect(nodes[r.src])
                rel = nodes[association.src].association.connect(nodes[association.dest])
                relation_type = ""
                if association.id in model.association_types:
                    relation_type = model.association_types[association.id]
                rel.association_type = relation_type
                rel.src_properties = association.src_props
                rel.dest_properties = association.dest_props
                rel.association_id = association.id
                rel.src_cardinality_lower_val = association.src_cardinality_lower_val
                rel.src_cardinality_upper_val = association.src_cardinality_upper_val
                rel.dest_cardinality_lower_val = association.dest_cardinality_lower_val
                rel.dest_cardinality_upper_val = association.dest_cardinality_upper_val
                # rel.dest_cardinality = r.dest_cardinality
                rel.save()
        for generalization in model.generalizations:
            if generalization.src is not None:
                rel = nodes[generalization.dest].generalization.connect(nodes[generalization.src])
                rel._type = generalization.relation_type
                rel.src_properties = []
                rel.dest_properties = []
                rel.generalization_id = generalization.id


class GeneralizationRel(StructuredRel):
    generalization_id = StringProperty()
    _type = StringProperty()
    src_properties = JSONProperty()
    dest_properties = JSONProperty()


class AssociationRel(StructuredRel):
    association_id = StringProperty()
    relation_type = "Association"
    association_type = StringProperty()
    src_cardinality_lower_val = StringProperty()
    src_cardinality_upper_val = StringProperty()
    dest_cardinality_lower_val = StringProperty()
    dest_cardinality_upper_val = StringProperty()
    src_properties = JSONProperty()
    dest_properties = JSONProperty()


class GeneralizationSet(StructuredNode):
    model_id = StringProperty()
    gs_id = UniqueIdProperty()
    name = StringProperty()
    attributes = ArrayProperty()


class Attribute(StructuredNode):
    model_id = StringProperty()
    attrib_id = UniqueIdProperty()
    name = StringProperty()
    attrib_type = StringProperty()


class AssociationNode(StructuredNode):
    model_id = StringProperty()
    node_id = UniqueIdProperty()
    association = Relationship("Class", "association", model=AssociationRel)

class Class(StructuredNode):
    model_id = StringProperty()
    class_id = UniqueIdProperty()
    name = StringProperty()
    type = StringProperty()
    generalization = Relationship("Class", "generalization", model=GeneralizationRel)
    association = Relationship("Class", "association", model=AssociationRel)
    attribute = Relationship("Attribute", "has")
