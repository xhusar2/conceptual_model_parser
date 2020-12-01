

class Attribute:
    name = ""
    id = ""
    attributes = []

    def __init__(self, attrib_id, name):
        self.name = name
        self.id = attrib_id

    def __str__(self):
        return f'id:{self.id} name: {self.name}' #parent: {self.parent_id}'