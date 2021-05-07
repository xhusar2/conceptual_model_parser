from exquiro.parsers.package_diagram_parser import PackageDiagramParser
from exquiro.models.package_diagram.package_node import PackageNode
from exquiro.models.package_diagram.package_relation import PackageRelation
from lxml import etree
import uuid


class OpenPonkPackageDiagramParser(PackageDiagramParser):
    def parse_nodes(self, model, namespaces):
        try:
            m_nodes = self.parse_packages(model, namespaces)
        except AttributeError as exc:
            raise exc
        except Exception as exc:
            raise Exception("Corrupted model in source file") from exc
        return m_nodes

    def parse_relations(self, model, namespaces):
        try:
            packages = self.get_packages(model, namespaces)
            m_relations = self.parse_imports(packages, namespaces)
            m_relations.update(self.parse_member_packages(packages, namespaces))
        except AttributeError as exc:
            raise exc
        except Exception as exc:
            raise Exception("Corrupted model in source file") from exc
        return m_relations

    def parse_id(self, model, namespaces):
        return str(uuid.uuid4())

    def parse_packages(self, model, namespaces):
        m_packages = set()
        packages = self.get_packages(model, namespaces)
        for package in packages:
            m_packages.add(self.parse_package(package, namespaces))
        return m_packages

    @staticmethod
    def parse_package(package, namespaces):
        try:
            node_id = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
            node_name = package.attrib["name"]
            node_class = "Package"
            if 'visibility' in package.attrib:
                node_visibility = package.attrib["visibility"]
            else:
                node_visibility = "public"
        except Exception as exc:
            raise AttributeError("Corrupted package node in source file") from exc
        return PackageNode(node_name, node_id, node_class, node_visibility)

    def parse_imports(self, packages, namespaces):
        m_imports = set()
        for package in packages:
            children = list(set(package.findall('.//packageImport[@xmi:type="uml:PackageImport"]', namespaces)) &
                            set(package.getchildren()))
            for child in children:
                m_imports.add(self.parse_import(child, package, namespaces))
        return m_imports

    @staticmethod
    def parse_import(package_import, package, namespaces):
        try:
            import_id = package_import.attrib["{" + namespaces['xmi'] + "}" + "id"]
            import_target = package_import.find(".//importedPackage").attrib["{" + namespaces['xmi'] + "}" + "idref"]
            import_source = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
            import_type = "PackageImport"
        except Exception as exc:
            raise AttributeError("Corrupted import relation in source file") from exc
        return PackageRelation(import_id, import_source, import_target, import_type)

    def parse_member_packages(self, packages, namespaces):
        m_members_of = set()
        for package in packages:
            children = package.getchildren()
            for child in children:
                if self.is_package(child, namespaces):
                    m_members_of.add(self.parse_member_package(child, package, namespaces))
        return m_members_of

    @staticmethod
    def parse_member_package(member_package, package, namespaces):
        try:
            # generate universal unique id
            member_id = str(uuid.uuid4())
            member_source = member_package.attrib["{" + namespaces['xmi'] + "}" + "id"]
            member_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
            member_type = "MemberOf"
        except Exception as exc:
            raise AttributeError("Corrupted package node or one of his child package node in source file") from exc
        return PackageRelation(member_id, member_source, member_target, member_type)

    def get_model(self, file_name, namespaces):
        return etree.parse(file_name).getroot().find('uml:Package', namespaces)

    @staticmethod
    def get_packages(model, namespaces):
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        packages.extend(model.findall('.//packagedElement[@xmi:type="uml:Model"]', namespaces))
        packages.append(model)
        return packages

    @staticmethod
    def is_package(element, namespaces):
        if "{" + namespaces['xmi'] + "}" + "type" not in element.attrib:
            return False
        el_type = element.attrib["{" + namespaces['xmi'] + "}" + "type"]
        return el_type == "uml:Package" or el_type == "uml:Model"
