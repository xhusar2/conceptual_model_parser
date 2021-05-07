class PackageNode:
    name = ""
    id = ""
    node_type = ""
    visibility = ""

    def __init__(self, name, node_id, node_type, visibility):
        self.name = name
        self.id = node_id
        self.node_type = node_type
        self.visibility = visibility
