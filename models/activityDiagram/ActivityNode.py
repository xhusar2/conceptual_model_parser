class ActivityNode:
    name = ""
    id = ""
    node_type = ""
    visibility = ""
    ordering = ""

    def __init__(self, node_id, node_type, visibility, name=None, ordering=None):
        self.name = name
        self.id = node_id
        self.node_type = node_type
        self.visibility = visibility
        self.ordering = ordering

    def __str__(self):
        return f'id:{self.id} name: {self.name}'
