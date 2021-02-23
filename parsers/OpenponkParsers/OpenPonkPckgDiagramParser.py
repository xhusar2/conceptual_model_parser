from parsers.PckgDiagramParser import PckgDiagramParser
from models.packageDiagram.PckgNode import PckgNode
from models.packageDiagram.PckgRelation import PckgRelation
from lxml import etree
import uuid


class OpenPonkPckgDiagramParser(PckgDiagramParser):
    def parse_nodes(self, model, namespaces):
        m_nodes = self.parse_packages(model, namespaces)
        return m_nodes

    # TODO find all relations - so far -> import
    def parse_relations(self, model, namespaces):
        packages = self.get_packages(model, namespaces)
        m_relations = self.parse_imports(packages, namespaces)
        m_relations.extend(self.parse_member_packages(packages, namespaces))
        return m_relations

    # TODO refactor
    def parse_id(self, model, namespaces):
        packaged_element = model.find('./packagedElement', namespaces)
        if packaged_element is not None:
            return packaged_element.attrib['{' + namespaces['xmi'] + '}' + 'id']
        id_attrib = '{' + namespaces['xmi'] + '}' + ':id'
        if id_attrib in model.attrib:
            return model.attrib[id_attrib]
        return ""

    def parse_packages(self, model, namespaces):
        m_packages = []
        packages = self.get_packages(model, namespaces)
        for package in packages:
            self.parse_package(package, namespaces, m_packages)
        return m_packages

    def parse_package(self, package, namespaces, packages: list):
        node_id = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
        node_name = package.attrib["name"]
        node_class = "Package"
        if 'visibility' in package.attrib:
            node_visibility = package.attrib["visibility"]
        else:
            node_visibility = "public"
        node = PckgNode(node_name, node_id, node_class, node_visibility)
        packages.append(node)
        return

    def parse_imports(self, packages, namespaces):
        m_imports = []
        for package in packages:
            self.parse_import(package, namespaces, m_imports)
        return m_imports

    def parse_import(self, package, namespaces, imports: list):
        children = package.getchildren()
        for child in children:
            if child.attrib["{" + namespaces['xmi'] + "}" + "type"] == "uml:PackageImport":
                import_id = child.attrib["{" + namespaces['xmi'] + "}" + "id"]
                import_source = child.getchildren()[0].attrib["{" + namespaces['xmi'] + "}" + "idref"]
                import_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
                import_type = "PackageImport"
                m_import = PckgRelation(import_id, import_source, import_target, import_type)
                imports.append(m_import)
        return

    def parse_member_packages(self, packages, namespaces):
        m_member_of = []
        for package in packages:
            self.parse_member_package(package, namespaces, m_member_of)
        return m_member_of

    def parse_member_package(self, package, namespaces, members):
        children = package.getchildren()
        for child in children:
            if child.attrib["{" + namespaces['xmi'] + "}" + "type"] == "uml:Package"\
                    or child.attrib["{" + namespaces['xmi'] + "}" + "type"] == "uml:Model":
                # need to generate unique id
                member_id = str(uuid.uuid4())
                member_target = child.attrib["{" + namespaces['xmi'] + "}" + "id"]
                member_source = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
                member_type = "MemberOf"
                m_member = PckgRelation(member_id, member_source, member_target, member_type)
                members.append(m_member)
        return

    def get_model(self, file_name, namespaces):
        return etree.parse(file_name).getroot().find('uml:Package', namespaces)

    @staticmethod
    def get_packages(model, namespaces):
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        packages.extend(model.findall('.//packagedElement[@xmi:type="uml:Model"]', namespaces))
        packages.append(model)
        return packages
