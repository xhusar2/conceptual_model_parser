class GeneralizationSet:
    name = ""
    id = ""
    attributes = []

    def __init__(self, name, gs_id, attributes):
        self.name = name
        self.id = gs_id
        self.attributes = attributes

    def __str__(self):
        return f'id:{self.id} name: {self.name} attributes: {self.attributes}'
