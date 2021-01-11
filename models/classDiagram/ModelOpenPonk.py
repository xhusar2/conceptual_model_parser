from models.classDiagram.Association import Association
from models.classDiagram.ClsDiagramModel import ClsDiagramModel
import re
from lxml import etree


class ClsDiagramModelOpenPonk(ClsDiagramModel):

    def __init__(self, file_name):
        super().__init__(file_name)

    def get_model_id(self):
        attrib_id = "{" + self.namespaces['xmi'] + "}" + "id"
        if attrib_id in self.model.attrib:
            return self.model.attrib[attrib_id]
        return ""

    def parse_types(self):
        c_types = {}
        a_types = {}
        class_types = etree.parse(self.model_file).getroot().findall('.//*[@base_Element]', self.namespaces)
        attrib_name = 'base_Element'
        for t in class_types:
            name = re.sub(r"\{.*\}", "", t.tag)
            self.class_types[t.attrib[attrib_name]] = name
            c_types[t.attrib[attrib_name]] = name

        # association types
        association_types = self.model.findall('.//*[@base_Association]', self.namespaces)
        for t in association_types:
            name = re.sub(r"\{.*\}", "", t.tag)
            self.association_types[t.attrib['base_Association']] = name
            a_types[t.attrib['base_Association']] = name
        return c_types, a_types

    def parse_association(self, a):
        model = self.get_model()
        src_prop, dest_prop = self.parse_owned_ends(a)
        assoc_id = a.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = ""
        if "name" in a.attrib:
            name = a.attrib["name"]

        src_prop["id"] = None
        dest_prop["id"] = None
        aggregation = "open_ponk_format"

        parts = a.attrib['memberEnd'].split(' ')
        src_prop["id"] = self.find_ref_element(model, parts[0])
        dest_prop["id"] = self.find_ref_element(model, parts[1])
        association = Association(assoc_id, name, src_prop, dest_prop)

        if aggregation != "none":
            association.relation_type = aggregation
        else:
            association.relation_type = "aggregation"
        self.associations.append(association)
        return association

    def parse_owned_ends(self, a):
        dest_prop = {}
        src_prop = {}
        owned_ends = a.findall('ownedEnd', self.namespaces)
        for o in owned_ends:
            # properties to find
            lval = o.find('lowerValue', self.namespaces)
            uval = o.find('upperValue', self.namespaces)
            if "dst" in (o.attrib["{" + self.namespaces['xmi'] + "}id"]):
                if lval is not None:
                    dest_prop["lowerValue"] = lval.attrib["value"]
                if uval is not None:
                    dest_prop["upperValue"] = uval.attrib["value"]
            elif "src" in (o.attrib["{" + self.namespaces['xmi'] + "}id"]):
                if lval is not None:
                    src_prop["lowerValue"] = lval.attrib["value"]
                if uval is not None:
                    src_prop["upperValue"] = uval.attrib["value"]

        return src_prop, dest_prop

    def parse_ownedEnds(self, a):
        dest_prop = {}
        src_prop = {}

        member_ends = a.attrib['memberEnd'].split()
        owned_ends = a.findall('ownedEnd', self.namespaces)

        for o in owned_ends:
            # properties to find
            lval = o.find('lowerValue', self.namespaces)
            uval = o.find('upperValue', self.namespaces)
            if member_ends[1] == (o.attrib["{" + self.namespaces['xmi'] + "}id"]):
                if lval is not None:
                    if 'value' in lval.attrib:
                        dest_prop["lowerValue"] = lval.attrib["value"]
                if uval is not None:
                    if 'value' in uval.attrib:
                        dest_prop["upperValue"] = uval.attrib["value"]
            elif member_ends[0] == (o.attrib["{" + self.namespaces['xmi'] + "}id"]):
                if lval is not None:
                    if 'value' in lval.attrib:
                        src_prop["lowerValue"] = lval.attrib["value"]
                if uval is not None:
                    if 'value' in uval.attrib:
                        src_prop["upperValue"] = uval.attrib["value"]
        return src_prop, dest_prop

    def find_ref_element(self, model, id_ref):
        xpath = './/*[@xmi:id="' + id_ref + '"]/@type'
        ref_element = model.xpath(xpath, namespaces=self.namespaces)[0]
        return ref_element
