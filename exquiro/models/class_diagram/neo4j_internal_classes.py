from neomodel import StructuredNode, StringProperty, ArrayProperty, Relationship, config, StructuredRel, JSONProperty, \
    UniqueIdProperty


class BaseNode(StructuredNode):
    model_metadata = JSONProperty()


class BaseRelation(StructuredRel):
    model_metadata = JSONProperty()


class GeneralizationRel(BaseRelation):
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
