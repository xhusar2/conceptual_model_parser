class AssociationClass:
    node_id = ""

    def __init__(self, node_id):
        self.node_id = node_id

    def __str__(self):
        return f'id:{self.node_id}'
