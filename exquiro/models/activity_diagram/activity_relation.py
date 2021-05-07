class ActivityRelation:
    source = ""
    target = ""
    id = ""
    relation_type = ""
    guard = ""

    def __init__(self, relation_id, source, target, relation_type, guard=None):
        self.id = relation_id
        self.source = source
        self.target = target
        self.relation_type = relation_type
        self.guard = guard
