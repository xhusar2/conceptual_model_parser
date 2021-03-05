from ..class_diagram_parser import ClsDiagramParser
from ...models.class_diagram.attribute import Attribute
from ...models.class_diagram.association import Association
from ...models.class_diagram.association_node import AssociationNode
from ...models.class_diagram.generalization_set import GeneralizationSet
from ...models.class_diagram.generalization import Generalization
from ...models.class_diagram.attribute import Attribute
from ...models.class_diagram.class_node import ClassNode
from ...models.class_diagram.association_class import AssociationClass
from ...models.class_diagram.association_class_connection import AssociationClassConnection
import re


class EaClsDiagramParser(ClsDiagramParser):

    # Input: xmi/xml file
    # Output parsed model ready to be stored to Neo4j
    def parse_file(self, file_name):
        namespaces = self.get_namespaces(file_name)
        model = self.get_model(file_name, namespaces)
        return self.parse_model(model, namespaces)

    def parse_id(self, model, namespaces):
        packaged_element = model.find('./packagedElement', namespaces)
        if packaged_element is not None:
            return packaged_element.attrib['{' + namespaces['xmi'] + '}' + 'id']
        id_attrib = '{' + namespaces['xmi'] + '}' + ':id'
        if id_attrib in model.attrib:
            return model.attrib[id_attrib]
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
        association_classes = model.findall('.//packagedElement[@xmi:type="uml:AssociationClass"]', namespaces)
        # associations
        for a in associations:
            parsed_associations, parsed_association_nodes = self.parse_association(a, model, namespaces)
            m_associations.extend(parsed_associations)
            m_association_nodes.extend(parsed_association_nodes)
        # association class
        for ac in association_classes:
            parsed_associations, parsed_association_nodes = self.parse_association(ac, model, namespaces)
            m_associations.extend(parsed_associations)
            m_association_nodes.extend(parsed_association_nodes)
        return m_associations, m_association_nodes

    def parse_association_classes(self, model, namespaces):
        m_association_classes = []
        m_association_class_connections = []
        association_classes = model.findall('.//packagedElement[@xmi:type="uml:AssociationClass"]', namespaces)
        for ac in association_classes:
            parsed_association_class, parsed_association_class_connections =  self.parse_association_class(ac, model, namespaces)
            m_association_classes.append(parsed_association_class)
            m_association_class_connections.extend(parsed_association_class_connections)
        return m_association_classes, m_association_class_connections

    def parse_association_class(self, ac, model, namespaces):
        # parse associations
        # create association class
        # correctly connect all nodes
        association_class_connections = []

        assoc_class_id = ac.attrib["{" + namespaces['xmi'] + "}" + "id"]
        name = ac.attrib["name"] if "name" in ac.attrib else ""
        association_class = AssociationClass(assoc_class_id)
        member_ends = ac.findall('memberEnd', namespaces)
        for m in member_ends:
            id_ref = m.attrib["{" + namespaces['xmi'] + "}" + "idref"]
            dest = self.find_ref_element(model, id_ref, namespaces)
            src = association_class.node_id
            association_class_connection = AssociationClassConnection(assoc_class_id, name, src, dest)
            association_class_connections.append(association_class_connection)

        association_class_refs = model.findall('.//packagedElement[@xmi:type="uml:Class"]', namespaces)
        for acr in association_class_refs:
            if acr.attrib["name"] == name:
                dest = acr.attrib["{" + namespaces['xmi'] + "}" + "id"]
                src = association_class.node_id
                association_class_connection = AssociationClassConnection(assoc_class_id, name, src, dest)
                association_class_connections.append(association_class_connection)

        return association_class, association_class_connections






    def parse_association(self, a, model, namespaces):
        associations = []
        association_nodes = []
        src_prop, dest_prop = self.parse_owned_ends(a, namespaces)
        assoc_id = a.attrib["{" + namespaces['xmi'] + "}" + "id"]
        name = a.attrib["name"] if "name" in a.attrib else ""

        src_prop["id"] = None
        dest_prop["id"] = None
        aggregation = 'none'

        # memberends
        member_ends = a.findall('memberEnd', namespaces)
        if len(member_ends) > 2:
            association_node = AssociationNode(assoc_id + "_ANode")
            for m in member_ends:
                id_ref = m.attrib["{" + namespaces['xmi'] + "}" + "idref"]
                if aggregation != "none":
                    aggregation = \
                        model.xpath('.//*[@xmi:id="' + id_ref + '"]/@aggregation', namespaces=namespaces)[0]
                dest_prop['id'] = self.find_ref_element(model, id_ref, namespaces)
                src_prop['id'] = association_node.node_id
                association = Association(assoc_id, name, src_prop, dest_prop)
                association.relation_type = aggregation if aggregation != "none" else "aggregation"
                associations.append(association)
            association_nodes.append(association_node)
        else:
            for m in member_ends:
                id_ref = m.attrib["{" + namespaces['xmi'] + "}" + "idref"]
                if aggregation != "none":
                    aggregation = \
                        model.xpath('.//*[@xmi:id="' + id_ref + '"]/@aggregation', namespaces=namespaces)[0]
                if 'src' in id_ref:
                    src_prop["id"] = self.find_ref_element(model, id_ref, namespaces)
                if 'dst' in id_ref:
                    dest_prop["id"] = self.find_ref_element(model, id_ref, namespaces)

            association = Association(assoc_id, name, src_prop, dest_prop)
            association.relation_type = aggregation if aggregation != "none" else "aggregation"
            associations.append(association)
        return associations, association_nodes

    def parse_types(self, model, namespaces):
        c_types = {}
        a_types = {}

        # class types
        class_types = model.findall('.//*[@base_Class]', namespaces)
        attrib_name = 'base_Class'
        for t in class_types:
            name = re.sub(r"{.*\}", "", t.tag)
            # self.class_types[t.attrib[attrib_name]] = name
            c_types[t.attrib[attrib_name]] = name

        # association types
        association_types = model.findall('.//*[@base_Association]', namespaces)
        for t in association_types:
            name = re.sub(r"{.*\}", "", t.tag)
            # self.association_types[t.attrib['base_Association']] = name
            a_types[t.attrib['base_Association']] = name
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

    def parse_owned_ends(self, a, namespaces):
        dest_prop = {}
        src_prop = {}
        owned_ends = a.findall('ownedEnd', namespaces)
        for o in owned_ends:
            # properties to find
            lval = o.find('lowerValue', namespaces)
            uval = o.find('upperValue', namespaces)
            if "dst" in (o.attrib["{" + namespaces['xmi'] + "}id"]):
                if lval is not None:
                    dest_prop["lowerValue"] = lval.attrib["value"]
                if uval is not None:
                    dest_prop["upperValue"] = uval.attrib["value"]
            elif "src" in (o.attrib["{" + namespaces['xmi'] + "}id"]):
                if lval is not None:
                    src_prop["lowerValue"] = lval.attrib["value"]
                if uval is not None:
                    src_prop["upperValue"] = uval.attrib["value"]
        return src_prop, dest_prop

    def parse_attribute(self, attribute, namespaces):
        attrib_id = attribute.attrib["{" + namespaces['xmi'] + "}" + "id"]
        name = ""
        if "name" in attribute.attrib:
            name = attribute.attrib["name"]
        return Attribute(attrib_id, name)

    def find_ref_element(self, model, id_ref, namespaces):
        xpath = './/*[@xmi:id="' + id_ref + '"]/type/@xmi:idref'
        ref_element = model.xpath(xpath, namespaces=namespaces)[0]
        return ref_element
