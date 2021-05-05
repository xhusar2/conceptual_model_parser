class Enumeration:
    name = ""
    id = ""
    values = []

    def __init__(self, attrib_id, name, values):
        self.name = name
        self.id = attrib_id
        self.values = values

    def __str__(self):
        return f'id:{self.id} name: {self.name}'