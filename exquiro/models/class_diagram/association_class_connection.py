from .relation import Relation


class AssociationClassConnection(Relation):

    def __init__(self, connection_id, name, src, dest):
        super().__init__(connection_id, name, src, dest, "Association_class_connection")
