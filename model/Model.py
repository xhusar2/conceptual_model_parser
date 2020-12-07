from lxml import etree
from model.Node import Node
from model.Association import Association
from model.Generalization import Generalization
from model.Attribute import Attribute
from model.GeneralizationSet import GeneralizationSet

import re

import json

class Model:

    namespaces = {'xmi': 'http://schema.omg.org/spec/XMI/2.1',
                  'uml': 'http://schema.omg.org/spec/UML/2.1'}
    type_attrib = "{" + namespaces['xmi'] + "}type"
    #type_value_generalization = "uml:Generalization"
    #type_value_association = "uml:Association"

    def __init__(self, name, model_file):
        self.name = name
        self.model_file = model_file
        self.nodes = []
        self.relations = []
        self.generalization_sets = []
        self.class_types = {}
        self.association_types = {}
        self.model = self.get_model()
        self.parse_model()

    def parse_types(self):
        class_types = self.model.findall('.//*[@base_Class]', self.namespaces)
        #print("here")
        for t in class_types:
            name = re.sub(r"\{.*\}","", t.tag)
            #print(name, t.attrib['base_Class'])
            #self.class_types.append(ClassType(t.attrib['base_Class'], name))
            self.class_types[t.attrib['base_Class']] = name

        #association types
        association_types = self.model.findall('.//*[@base_Association]', self.namespaces)
        for t in association_types:
            name = re.sub(r"\{.*\}","", t.tag)
            self.association_types[t.attrib['base_Association']] = name
            #print(name, t.attrib['base_Association'])

            #self.association_types.append(AssociationType(t.attrib['base_Association'], name))



    def parse_model(self):
        self.parse_classes()
        self.parse_associations()
        self.parse_generalization_sets()
        self.parse_types()


    def parse_generalization_sets(self):
        gsets = self.model.findall('.//packagedElement[@xmi:type="uml:GeneralizationSet"]', self.namespaces)
        for g in gsets:
            self.parse_gset(g)

    def parse_gset(self, gs):
        gs_id = gs.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = gs.attrib["name"]
        attributes = {}
        attributes['complete'] = bool(gs.attrib["isCovering"])
        attributes['disjoint'] = bool(gs.attrib["isDisjoint"])
        generalizations = gs.findall('./generalization', self.namespaces)
        attributes['generalizations'] = []
        for g in generalizations:
            g_id = g.attrib["{" + self.namespaces['xmi'] + "}" + "idref"]
            attributes['generalizations'].append(g_id)

        gset = GeneralizationSet(name, gs_id, attributes)
        self.generalization_sets.append(gset)

    def parse_classes(self):
        classes = self.model.findall('.//packagedElement[@xmi:type="uml:Class"]', self.namespaces)
        for c in classes:
            self.parse_class(c)

    def parse_class(self, c):
        parsed_attributes = self.parse_attributes(c)
        #new node
        node_id = c.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        n = Node(c.attrib["name"], node_id, "uml:Class", parsed_attributes)
        #print(n)
        self.nodes.append(n)
        #parse sub classes, if present
        nestedClassifiers = c.findall('nestedClassifier', namespaces=self.namespaces)
        for nc in nestedClassifiers:
            if self.type_attrib in nc.attrib and nc.attrib[self.type_attrib] == "uml:Class":
                self.parse_class(nc)
        #parse generalization, if present
        generalization = c.find('generalization', namespaces=self.namespaces)
        if generalization is not None:
            self.parse_generalization(generalization, node_id)

    def parse_attributes(self, c):
        result = []
        attributes = c.findall('ownedAttribute', self.namespaces)
        for a in attributes:
            #attrib_id, value = self.parse_attribute(a)
            #result[attrib_id] = value
            result.append(self.parse_attribute(a))
        return result

    def parse_association(self, a):
        model = self.get_model()
        src_prop, dest_prop = self.parse_ownedEnds(a)
        assoc_id = a.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = ""
        if "name" in a.attrib:
            name = a.attrib["name"]
        # memberends
        memberends = a.findall('memberEnd', self.namespaces)
        src_prop["id"] = None
        dest_prop["id"] = None
        aggregation = 'none'
        for m in memberends:
            idref = m.attrib["{" + self.namespaces['xmi'] + "}" + "idref"]
            aggregation = model.xpath('.//*[@xmi:id="' + idref + '"]/@aggregation', namespaces=self.namespaces)[0]
            if 'src' in idref:
                src_prop["id"] = self.find_ref_element(model, idref)
            if 'dst' in idref:
                dest_prop["id"] = self.find_ref_element(model, idref)
                #print(dst)
        association = Association(assoc_id, name, src_prop, dest_prop)

        if aggregation != "none":
            association.relation_type = aggregation
        else:
            association.relation_type = "aggregation"
        #print(association)
        self.relations.append(association)
        return association

    def parse_ownedEnds(self, a):
        dest_prop = {}
        src_prop = {}
        ownedEnds = a.findall('ownedEnd', self.namespaces)
        for o in ownedEnds:
            #properties to find
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

    def parse_generalization(self, generalization, node_id):
        generalization_id = generalization.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = "Generalization"
        src = generalization.attrib["general"]
        dest = node_id
        r = Generalization(generalization_id, name, src, dest)
        self.relations.append(r)
        return r

    def parse_attribute(self, attribute):
        attrib_id = attribute.attrib["{" + self.namespaces['xmi'] + "}" + "id"]
        name = ""
        if "name" in attribute.attrib:
            name = attribute.attrib["name"]
        a = Attribute(attrib_id, name)
        #print(json.dumps(a.__dict__))
        return a #attrib_id, a
    
    def get_model(self):
        return etree.parse(self.model_file).find('uml:Model', self.namespaces)

    def parse_associations(self):
        # find model
        model = self.get_model()
        associations = model.findall('.//packagedElement[@xmi:type="uml:Association"]', self.namespaces)
        for a in associations:
            self.parse_association(a)


    def find_ref_element(self, model, idref):
        xpath = './/*[@xmi:id="' + idref + '"]/type/@xmi:idref'
        ref_element = model.xpath(xpath, namespaces=self.namespaces)[0]
        return ref_element








