class PackageRelation:
    source = ""
    target = ""
    id = ""
    relation_type = ""

    def __init__(self, relation_id, from_node, to_node, relation_type):
        self.id = relation_id
        self.source = from_node
        self.target = to_node
        self.relation_type = relation_type
