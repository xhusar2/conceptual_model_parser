from parsers.PackageDiagramParser import PackageDiagramParser
from models.packageDiagram.PackageNode import PackageNode
from models.packageDiagram.PackageRelation import PackageRelation
from lxml import etree
import uuid


class VPPackageParser(PackageDiagramParser):

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
            m_relations = self.parse_dependencies(model, namespaces)
            m_relations.extend(self.parse_imports(model, namespaces))
            m_relations.extend(self.parse_merges(model, namespaces))
            packages = self.get_packages(model, namespaces)
            m_relations.extend(self.parse_member_packages(packages, namespaces))
        except AttributeError as exc:
            raise exc
        except Exception as exc:
            raise Exception("Corrupted model in source file") from exc
        return m_relations

    def parse_id(self, model, namespaces):
        if '{' + namespaces['xmi'] + '}' + 'id' not in model.attrib:
            return uuid.uuid4()
        else:
            return model.attrib['{' + namespaces['xmi'] + '}' + 'id']

    def parse_packages(self, model, namespaces):
        m_packages = []
        packages = self.get_packages(model, namespaces)
        for package in packages:
            m_packages.append(self.parse_package(package, namespaces))
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

    @staticmethod
    def parse_supplier_client_relation(relation, namespaces, rel_type):
        try:
            relation_id = relation.attrib["{" + namespaces['xmi'] + "}" + "id"]
            relation_target = relation.attrib["supplier"]
            relation_source = relation.attrib["client"]
            relation_type = rel_type
        except Exception as exc:
            raise AttributeError("Corrupted " + rel_type + " relation in source file") from exc
        return PackageRelation(relation_id, relation_source, relation_target, relation_type)

    def parse_dependencies(self, model, namespaces):
        m_dependencies = []
        dependencies = model.findall('.//ownedMember[@xmi:type="uml:Dependency"]', namespaces)
        for dependency in dependencies:
            m_dependencies.append(self.parse_supplier_client_relation(dependency, namespaces, "Dependency"))
        return m_dependencies

    def parse_merges(self, model, namespaces):
        m_merge = []
        merges = model.findall('.//packageMerge', namespaces)
        for merge in merges:
            m_merge.append(self.parse_supplier_client_relation(merge, namespaces, "PackageMerge"))
        return m_merge

    def parse_imports(self, model, namespaces):
        m_imports = []
        imports = model.findall('.//packageImport', namespaces)
        for import_e in imports:
            m_imports.append(self.parse_import(import_e, namespaces))
        return m_imports

    @staticmethod
    def parse_import(import_element, namespaces):
        try:
            import_id = import_element.attrib["{" + namespaces['xmi'] + "}" + "id"]
            import_target = import_element.attrib["supplier"]
            import_source = import_element.attrib["client"]
            applied_stereotype = import_element.find('.//appliedStereotype', namespaces)
            if applied_stereotype.attrib["{" + namespaces['xmi'] + "}" + "value"] == "Dependency_import_id":
                import_type = "PackageImport"
            else:
                import_type = "PackageAccess"
        except Exception as exc:
            raise AttributeError("Corrupted package import relation in source file") from exc
        return PackageRelation(import_id, import_source, import_target, import_type)

    def parse_member_packages(self, packages, namespaces):
        m_member_of = []
        for package in packages:
            children = package.getchildren()
            for child in children:
                if self.is_package(child, namespaces):
                    m_member_of.append(self.parse_member_package(child, package, namespaces))
        return m_member_of

    @staticmethod
    def parse_member_package(child, package, namespaces):
        try:
            # need to generate unique id
            member_id = str(uuid.uuid4())
            member_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
            member_source = child.attrib["{" + namespaces['xmi'] + "}" + "id"]
            member_type = "MemberOf"
        except Exception as exc:
            raise AttributeError("Corrupted package node or one of its child package nodes in source file") from exc
        return PackageRelation(member_id, member_source, member_target, member_type)

    def get_model(self, file_name, namespaces):
        model = etree.parse(file_name).getroot().find('uml:Model', namespaces)
        if model is None:
            raise AttributeError("Corrupted source file, no model found")
        return model

    @staticmethod
    def get_packages(model, namespaces):
        packages = model.findall('.//ownedMember[@xmi:type="uml:Package"]', namespaces)
        packages.extend(model.findall('.//ownedMember[@xmi:type="uml:Model"]', namespaces))
        return packages

    @staticmethod
    def is_package(element, namespaces):
        if "{" + namespaces['xmi'] + "}" + "type" not in element.attrib:
            return False
        element_type = element.attrib["{" + namespaces['xmi'] + "}" + "type"]
        return element_type == "uml:Package" or element_type == "uml:Model"
