from model.Relation import Relation


class Generalization(Relation):

    def __init__(self, association_id, name, src_id, dest_id):
        super().__init__( association_id, name, src_id, dest_id, "Generalization")