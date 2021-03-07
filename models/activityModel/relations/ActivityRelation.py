class ActivityRelation:
    src = ""
    dest = ""
    id = ""
    relation_type = ""
    guard = ""

    def __init__(self, relation_id, from_node, to_node, relation_type, guard=None):
        self.id = relation_id
        self.src = from_node
        self.dest = to_node
        self.relation_type = relation_type
        self.guard = guard
