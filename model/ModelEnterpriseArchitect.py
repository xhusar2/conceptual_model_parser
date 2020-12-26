from model.Association import Association
from model.Model import Model
import re


class ModelEnterpriseArchitect(Model):

    def __init__(self, file_name):
        super().__init__(file_name)

    def get_model_id(self):
        packaged_element = self.model.find('./packagedElement', self.namespaces)
        if packaged_element is not None:
            # print(packagedElement)
            # print(packagedElement.attrib)
            return packaged_element.attrib['{' + self.namespaces['xmi'] + '}' + 'id']
        id_attrib = '{' + self.namespaces['xmi'] + '}' + ':id'
        if id_attrib in self.model.attrib:
            return self.model.attrib[id_attrib]
        return ""

    def parse_types(self):
        c_types = {}
        a_types = {}

        # class types
        class_types = self.model.findall('.//*[@base_Class]', self.namespaces)
        attrib_name = 'base_Class'
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

    def parse_model(self):
        self.get_model_id()
        self.parse_classes()
        self.parse_associations()
        self.parse_generalization_sets()
        self.parse_types()

    def find_ref_element(self, model, id_ref):
        xpath = './/*[@xmi:id="' + id_ref + '"]/type/@xmi:idref'
        ref_element = model.xpath(xpath, namespaces=self.namespaces)[0]
        return ref_element

    def parse_association(self, a):
        model = self.get_model()
        src_prop, dest_prop = self.parse_owned_ends(a)
        assoc_id = a.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = a.attrib["name"] if "name" in a.attrib else ""

        # memberends
        member_ends = a.findall('memberEnd', self.namespaces)

        src_prop["id"] = None
        dest_prop["id"] = None
        aggregation = 'none'

        for m in member_ends:
            id_ref = m.attrib["{" + self.namespaces['xmi'] + "}" + "idref"]
            if aggregation != "none":
                aggregation = model.xpath('.//*[@xmi:id="' + id_ref + '"]/@aggregation', namespaces=self.namespaces)[0]
            if 'src' in id_ref:
                src_prop["id"] = self.find_ref_element(model, id_ref)
            if 'dst' in id_ref:
                dest_prop["id"] = self.find_ref_element(model, id_ref)
        association = Association(assoc_id, name, src_prop, dest_prop)
        association.relation_type = aggregation if aggregation != "none" else "aggregation"

        self.associations.append(association)
        return association
