import xml.etree.ElementTree as ET
from models.classDiagram.Relation import Relation


class Association(Relation):

    src_props = {}
    dst_props = {}
    src_cardinality_lower_val = None
    src_cardinality_upper_val = None
    dest_cardinality_lower_val = None
    dest_cardinality_upper_val = None

    def __init__(self, association_id, name, src_props, dest_props):
        super().__init__( association_id, name, src_props['id'], dest_props['id'], "Association")
        src_props.pop('id')
        dest_props.pop('id')
        if 'lowerValue' in src_props:
            #self.src_cardinality = (src_props['lowerValue'], src_props['upperValue'])
            self.src_cardinality_lower_val = src_props['lowerValue']
            src_props.pop('lowerValue')
        if 'upperValue' in src_props:
            self.src_cardinality_upper_val = src_props['upperValue']
            src_props.pop('upperValue')
        if 'lowerValue' in dest_props:
            self.dest_cardinality_lower_val = dest_props['lowerValue']
            dest_props.pop('lowerValue')
        if 'upperValue' in dest_props:
            self.dest_cardinality_upper_val = dest_props['upperValue']
            dest_props.pop('upperValue')
            #self.dest_cardinality = (dest_props['lowerValue'], dest_props['upperValue'])
        self.src_props = src_props
        self.dest_props = dest_props


    def __str__(self):
        return f'id:{self.id} name: {self.name} src_id: {self.src} dest_id: {self.dest } props{[str(p) for p in self.src_props.values()]}'
