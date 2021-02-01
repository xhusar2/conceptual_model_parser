

class PckgRelation:
    src = ""
    dest = ""
    id = ""
    relation_type = ""

    def __init__(self, relation_id, from_node, to_node, relation_type):
        self.id = relation_id
        self.src = from_node
        self.dest = to_node
        self.relation_type = relation_type

    def __str__(self):
        return f'id:{self.id} name: {self.name} src_id: {self.src} dest_id: {self.dest} relation_type:{self.relation_type}'