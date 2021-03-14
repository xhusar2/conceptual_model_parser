from parsers.PackageDiagramParser import PackageDiagramParser
from models.packageDiagram.PackageNode import PackageNode
from models.packageDiagram.PackageRelation import PackageRelation
from lxml import etree
import uuid


class EAPackageDiagramParser(PackageDiagramParser):

    def parse_nodes(self, model, namespaces):
        nodes = self.parse_packages(model, namespaces)
        return nodes

    def parse_relations(self, model, namespaces):
        packages = self.get_packages(model, namespaces)
        relations = self.parse_dependencies(model, namespaces)
        relations.extend(self.parse_merges(packages, namespaces))
        relations.extend(self.parse_imports(packages, namespaces))
        relations.extend(self.parse_member_packages(packages, namespaces))
        relations.extend(self.parse_usages(model, namespaces))
        return relations

    def parse_id(self, model, namespaces):
        return str(uuid.uuid4())

    def parse_packages(self, model, namespaces):
        m_packages = []
        packages = self.get_packages(model, namespaces)
        for package in packages:
            m_packages.append(self.parse_package(package, namespaces))
        return m_packages

    @staticmethod
    def parse_package(package, namespaces):
        node_id = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
        node_name = package.attrib["name"]
        node_class = "Package"
        node_visibility = package.attrib["visibility"]
        return PackageNode(node_name, node_id, node_class, node_visibility)

    def parse_dependencies(self, model, namespaces):
        m_dependencies = []
        dependencies = model.findall('.//packagedElement[@xmi:type="uml:Dependency"]', namespaces)
        for dependency in dependencies:
            m_dependencies.append(self.parse_dependency(dependency, namespaces))
        return m_dependencies

    @staticmethod
    def parse_dependency(dependency, namespaces):
        dependency_id = dependency.attrib["{" + namespaces['xmi'] + "}" + "id"]
        dependency_source = dependency.attrib["supplier"]
        dependency_target = dependency.attrib["client"]
        dependency_type = "Dependency"
        return PackageRelation(dependency_id, dependency_source, dependency_target, dependency_type)

    def parse_merges(self, packages, namespaces):
        m_merges = []
        for package in packages:
            children = package.getchildren()
            for child in children:
                if child.attrib["{" + namespaces['xmi'] + "}" + "type"] == "uml:PackageMerge":
                    m_merges.append(self.parse_merge(child, package, namespaces))
        return m_merges

    @staticmethod
    def parse_merge(package_merge, package, namespaces):
        merge_id = package_merge.attrib["{" + namespaces['xmi'] + "}" + "id"]
        merge_target = package_merge.attrib["mergedPackage"]
        merge_source = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
        merge_type = "PackageMerge"
        return PackageRelation(merge_id, merge_source, merge_target, merge_type)

    def parse_imports(self, packages, namespaces):
        m_imports = []
        for package in packages:
            children = package.getchildren()
            for child in children:
                if child.attrib["{" + namespaces['xmi'] + "}" + "type"] == "uml:PackageImport":
                    m_imports.append(self.parse_import(child, package, namespaces))
        return m_imports

    @staticmethod
    def parse_import(package_import, package, namespaces):
        import_id = package_import.attrib["{" + namespaces['xmi'] + "}" + "id"]
        import_target = package_import.attrib["importedPackage"]
        import_source = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
        import_type = "PackageImport"
        return PackageRelation(import_id, import_source, import_target, import_type)

    def parse_member_packages(self, packages, namespaces):
        m_member_of = []
        for package in packages:
            children = package.getchildren()
            for child in children:
                if child.attrib["{" + namespaces['xmi'] + "}" + "type"] == "uml:Package":
                    m_member_of.append(self.parse_member_package(child, package, namespaces))
        return m_member_of

    @staticmethod
    def parse_member_package(child_package, package, namespaces):
        # need to generate unique id
        member_id = str(uuid.uuid4())
        member_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
        member_source = child_package.attrib["{" + namespaces['xmi'] + "}" + "id"]
        member_type = "MemberOf"
        return PackageRelation(member_id, member_source, member_target, member_type)

    def parse_usages(self, model, namespaces):
        m_usage = []
        usages = model.findall('.//packagedElement[@xmi:type="uml:Usage"]', namespaces)
        for usage in usages:
            m_usage.append(self.parse_usage(usage, namespaces))
        return m_usage

    @staticmethod
    def parse_usage(usage, namespaces):
        usage_id = usage.attrib["{" + namespaces['xmi'] + "}" + "id"]
        usage_target = usage.attrib["supplier"]
        usage_source = usage.attrib["client"]
        rel_type = "Usage"
        return PackageRelation(usage_id, usage_source, usage_target, rel_type)

    def get_model(self, file_name, namespaces):
        return etree.parse(file_name).getroot().find('uml:Model', namespaces)

    @staticmethod
    def get_packages(model, namespaces):
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        return packages
