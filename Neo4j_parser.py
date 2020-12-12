from neomodel import StructuredNode, StringProperty, ArrayProperty, RelationshipTo, RelationshipFrom, Relationship,\
    config, StructuredRel, JSONProperty, UniqueIdProperty
from neomodel import db as neodb
from model.Association import Association
from model.Generalization import Generalization
import json


config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'


class Model_parser:

    def __init__(self):
        pass

    def delete_all(self):
        neodb.cypher_query("MATCH ()-[r]-() DETACH DELETE r")
        neodb.cypher_query("MATCH (n) DETACH DELETE n")

    def add_to_db(self, model):
        nodes = {}
        count = 0
        for n in model.nodes:
            class_type = ""
            if n.id in model.class_types:
                class_type = model.class_types[n.id]
            node = Class(class_id=n.id, name=n.name, type=class_type, model_id=model.id)
            #print(n.name)
            nodes[n.id] = node
            node.save()
            for a in n.attributes:
                attrib = Attribute(attrib_id=a.id, name=a.name, model_id=model.id)
                #print(a.name, a.id)
                attrib.save()
                node.attribute.connect(attrib)

        count = 0
        for n in model.generalization_sets:
            #if n type is class
            node = GeneralizationSet(gs_id=n.id, name=n.name, attributes=[str(a) for a in n.attributes], model_id=model.id)
            #print(n.name)
            nodes[n.id] = node
            node.save()
            count += 1
            print(count)

        for r in model.relations:
            if isinstance(r, Association):
                if r.src in nodes and r.dest in nodes:
                    rel1 = nodes[r.dest].association.connect(nodes[r.src])
                    rel = nodes[r.src].association.connect(nodes[r.dest])
                    relation_type = ""
                    if r.id in model.association_types:
                        relation_type = model.association_types[r.id]
                    rel.association_type = relation_type
                    rel.src_properties = r.src_props
                    rel.dest_properties = r.dest_props
                    rel.association_id = r.id
                    rel.src_cardinality_lower_val = r.src_cardinality_lower_val
                    rel.src_cardinality_upper_val = r.src_cardinality_upper_val
                    rel.dest_cardinality_lower_val = r.dest_cardinality_lower_val
                    rel.dest_cardinality_upper_val = r.dest_cardinality_upper_val
                    #rel.dest_cardinality = r.dest_cardinality
                    rel.save()
            elif isinstance(r, Generalization):
                #print(r)
                if r.src is not None:
                    rel = nodes[r.dest].generalization.connect(nodes[r.src])
                    rel._type = r.relation_type
                    rel.src_properties = []
                    rel.dest_properties = []
                    rel.generalization_id = r.id


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
    #generalization = Relationship("Class", "generalization", model=GeneralizationRel)
    #association = Relationship("Class", "association", model=AssociationRel)
    attributes = ArrayProperty()


class Attribute(StructuredNode):
    model_id = StringProperty()
    attrib_id = UniqueIdProperty()
    name = StringProperty()
    attrib_type = StringProperty()



class Class(StructuredNode):
    model_id = StringProperty()
    class_id = UniqueIdProperty()
    name = StringProperty()
    type = StringProperty()
    generalization = Relationship("Class", "generalization", model=GeneralizationRel)
    association = Relationship("Class", "association", model=AssociationRel)
    #attributes = JSONProperty()
    attribute = Relationship("Attribute", "has")


