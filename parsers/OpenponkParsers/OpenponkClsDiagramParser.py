from models.classDiagram.ClsDiagramModel import ClsDiagramModel
from parsers.ClsDiagramParser import ClsDiagramParser
from models.classDiagram.ClassNode import ClassNode
from models.classDiagram.Association import Association
from models.classDiagram.AssociationNode import AssociationNode
from models.classDiagram.GeneralizationSet import GeneralizationSet
from models.classDiagram.Generalization import Generalization
from models.classDiagram.Attribute import Attribute
import re


class OpenponkClsDiagramParser(ClsDiagramParser):



    # Input: xmi/xml file
    # Output parsed model ready to be stored to Neo4j
    def parse_file(self, file_name):
        namespaces = self.get_namespaces(file_name)
        model = self.get_model(file_name, namespaces)
        root = self.get_root(file_name)
        return self.parse_model(model, root, namespaces)

    def parse_model(self, model, root, namespaces):
        m_id = self.parse_id(model, namespaces)
        m_classes = self.parse_classes(model, namespaces)
        m_associations, m_association_nodes = self.parse_associations(model, namespaces)
        m_generalizations = self.parse_generalizations(model, namespaces)
        c_types, a_types = self.parse_types(model, root, namespaces)
        m_gsets = self.parse_generalization_sets(model, namespaces)
        # TODO return neo4j model consisting from nodes and relations only
        #  implement in ClsDiagramModel
        return ClsDiagramModel(m_id, m_classes, m_associations, m_association_nodes
                               , m_generalizations, m_gsets, c_types, a_types)


    def parse_id(self, model, namespaces):
        attrib_id = "{" + namespaces['xmi'] + "}" + "id"
        if attrib_id in model.attrib:
            return model.attrib[attrib_id]
        return ""

    def parse_classes(self, model, namespaces):
        m_classes = []
        classes = model.findall('.//packagedElement[@xmi:type="uml:Class"]', namespaces)
        for c in classes:
            self.parse_class(c, namespaces, m_classes)
        return m_classes

    def parse_class(self, c, namespaces, classes: list):
        parsed_attributes = self.parse_attributes(c, namespaces)
        # new node
        node_id = c.attrib["{" + namespaces['xmi'] + "}" + "id"]
        n = ClassNode(c.attrib["name"], node_id, "uml:Class", parsed_attributes)
        classes.append(n)
        # parse sub classes, if present
        nested_classifiers = c.findall('nestedClassifier', namespaces=namespaces)
        for nc in nested_classifiers:
            if "{" + namespaces['xmi'] + "}type" in nc.attrib and nc.attrib[
                "{" + namespaces['xmi'] + "}type"] == "uml:Class":
                self.parse_class(nc, namespaces, classes)
        return

    def parse_generalizations(self, model, namespaces):
        m_generalizations = []
        classes = model.findall('.//packagedElement[@xmi:type="uml:Class"]', namespaces)
        for c in classes:
            self.parse_generalization(c, namespaces, m_generalizations)
        return m_generalizations

    def parse_generalization(self, c, namespaces, generalizations):
        # parse sub classes, if present
        node_id = c.attrib["{" + namespaces['xmi'] + "}" + "id"]
        nested_classifiers = c.findall('nestedClassifier', namespaces=namespaces)
        for nc in nested_classifiers:
            if "{" + namespaces['xmi'] + "}type" in nc.attrib \
                    and nc.attrib["{" + namespaces['xmi'] + "}type"] == "uml:Class":
                self.parse_generalization(nc, namespaces, generalizations)
        # parse generalization, if present
        generalization = c.find('generalization', namespaces=namespaces)
        if generalization is not None:
            generalization_id = generalization.attrib["{" + namespaces['xmi'] + "}" + "id"]
            name = "Generalization"
            src = generalization.attrib["general"]
            dest = node_id
            generalizations.append(Generalization(generalization_id, name, src, dest))
        return

    def parse_associations(self, model, namespaces):
        m_associations = []
        m_association_nodes = []
        associations = model.findall('.//packagedElement[@xmi:type="uml:Association"]', namespaces)
        for a in associations:
            parsed_associations, parsed_association_nodes = self.parse_association(a, model, namespaces)
            m_associations.extend(parsed_associations)
            m_association_nodes.extend(parsed_association_nodes)
        return m_associations, m_association_nodes

    def parse_association(self, a, model, namespaces):
        associations = []
        association_nodes = []
        assoc_id = a.attrib["{" + namespaces['xmi'] + "}" + "id"]
        name = a.attrib["name"] if "name" in a.attrib else ""
        src_prop = {}
        dest_prop = {}
        src_prop["id"] = None
        dest_prop["id"] = None
        aggregation = "open_ponk_format"

        # memberends
        member_ends = a.attrib['memberEnd'].split(' ')
        if len(member_ends) > 2:
            association_node = AssociationNode(assoc_id + "_ANode")
            for m in member_ends:
                id_ref = m.attrib["{" + namespaces['xmi'] + "}" + "idref"]
                if aggregation != "none":
                    aggregation = \
                        model.xpath('.//*[@xmi:id="' + id_ref + '"]/@aggregation', namespaces=namespaces)[0]
                dest_prop['id'] = self.find_ref_element(model, id_ref, namespaces)
                src_prop['id'] = association_node.node_id
                self.parse_owned_ends(a, src_prop, dest_prop, namespaces)
                association = Association(assoc_id, name, src_prop, dest_prop)
                association.relation_type = aggregation if aggregation != "none" else "aggregation"
                associations.append(association)
            association_nodes.append(association_node)
        else:
            src_prop["id"] = self.find_ref_element(model, member_ends[0], namespaces)
            dest_prop["id"] = self.find_ref_element(model, member_ends[1], namespaces)
            self.parse_owned_ends(a, src_prop, dest_prop, namespaces)
            association = Association(assoc_id, name, src_prop, dest_prop)
            association.relation_type = aggregation if aggregation != "none" else "aggregation"
            associations.append(association)
        return associations, association_nodes

    def parse_types(self, model, root, namespaces):
        c_types = {}
        a_types = {}

        # class types
        class_types = root.findall('.//*[@base_Element]', namespaces)
        attrib_name = 'base_Element'
        for t in class_types:
            name = re.sub(r"{.*\}", "", t.tag)
            # self.class_types[t.attrib[attrib_name]] = name
            c_types[t.attrib[attrib_name]] = name

        # association types
        association_types = root.findall('.//*[@base_Element]', namespaces)
        for t in association_types:
            name = re.sub(r"{.*\}", "", t.tag)
            # self.association_types[t.attrib['base_Association']] = name
            a_types[t.attrib['base_Element']] = name
        return c_types, a_types

    def parse_generalization_sets(self, model, namespaces):
        m_gsets = []
        gsets = model.findall('.//packagedElement[@xmi:type="uml:GeneralizationSet"]', namespaces)
        for g in gsets:
            m_gsets.append(self.parse_gset(g, namespaces))
        return m_gsets

    def parse_gset(self, gs, namespaces):
        gs_id = gs.attrib["{" + namespaces['xmi'] + "}" + "id"]
        name = gs.attrib["name"]
        attributes = {'complete': bool(gs.attrib["isCovering"]), 'disjoint': bool(gs.attrib["isDisjoint"])}
        generalizations = gs.findall('./generalization', namespaces)
        attributes['generalizations'] = []
        for g in generalizations:
            g_id = g.attrib["{" + namespaces['xmi'] + "}" + "idref"]
            attributes['generalizations'].append(g_id)

        gset = GeneralizationSet(name, gs_id, attributes)
        return gset

    def parse_attributes(self, c, namespaces):
        c_attributes = []
        attributes = c.findall('ownedAttribute', namespaces)
        for a in attributes:
            c_attributes.append(self.parse_attribute(a, namespaces))
        return c_attributes

    def parse_owned_ends(self, a, src_prop, dest_prop, namespaces):
        owned_ends = a.findall('ownedEnd', namespaces)
        for o in owned_ends:
            # properties to find
            lval = o.find('lowerValue', namespaces)
            uval = o.find('upperValue', namespaces)
            if dest_prop["id"] in (o.attrib["type"]):
                if lval is not None and "value" in  lval.attrib:
                    dest_prop["lowerValue"] = lval.attrib["value"]
                if uval is not None and "value" in  uval.attrib:
                    dest_prop["upperValue"] = uval.attrib["value"]
            elif src_prop["id"] in (o.attrib["type"]):
                if lval is not None and "value" in  lval.attrib:
                    src_prop["lowerValue"] = lval.attrib["value"]
                if uval is not None and "value" in  uval.attrib:
                    src_prop["upperValue"] = uval.attrib["value"]
        return

    def parse_attribute(self, attribute, namespaces):
        attrib_id = attribute.attrib["{" + namespaces['xmi'] + "}" + "id"]
        name = ""
        if "name" in attribute.attrib:
            name = attribute.attrib["name"]
        return Attribute(attrib_id, name)

    def find_ref_element(self, model, id_ref, namespaces):
        xpath = './/*[@xmi:id="' + id_ref + '"]/@type'
        ref_element = model.xpath(xpath, namespaces=namespaces)[0]
        return ref_element
