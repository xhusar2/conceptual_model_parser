

class PckgNode:
    name = ""
    id = ""
    node_class = ""
    visibility = ""
    attributes = []

    def __init__(self, name, node_id, node_class, visibility, attributes=None):
        self.name = name
        self.id = node_id
        self.node_class = node_class
        self.visibility = visibility
        self.attributes = attributes

    def __str__(self):
        return f'id:{self.id} name: {self.name} attributes: {self.attributes}'
