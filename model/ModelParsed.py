# unified model after file parsing
# this model has all attributes filled and is ready to be stored to the neo4j database


class ModelParsed:
    def __init__(self, model_id, classes, associations, generalizations, generalization_sets, c_types, a_types):
        self.id = model_id
        self.classes = classes
        self.associations = associations
        self.generalizations = generalizations
        self.generalization_sets = generalization_sets
        self.class_types = c_types
        self.association_types = a_types
