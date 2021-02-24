from parsers.PckgDiagramParser import PckgDiagramParser
from models.packageDiagram.PckgNode import PckgNode
from models.packageDiagram.PckgRelation import PckgRelation
from lxml import etree
import uuid


class EAPckgDiagramParser(PckgDiagramParser):

    def parse_nodes(self, model, namespaces):
        m_nodes = self.parse_packages(model, namespaces)
        return m_nodes

    # TODO find all relations - so far -> dependency, import, merge, nestingPackage
    def parse_relations(self, model, namespaces):
        packages = self.get_packages(model, namespaces)
        m_relations = self.parse_dependencies(model, namespaces)
        m_relations.extend(self.parse_merges(packages, namespaces))
        m_relations.extend(self.parse_imports(packages, namespaces))
        m_relations.extend(self.parse_member_packages(packages, namespaces))
        m_relations.extend(self.parse_usages(model, namespaces))
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
        node_visibility = package.attrib["visibility"]
        node = PckgNode(node_name, node_id, node_class, node_visibility)
        packages.append(node)
        return

    def parse_dependencies(self, model, namespaces):
        m_dependencies = []
        dependencies = model.findall('.//packagedElement[@xmi:type="uml:Dependency"]', namespaces)
        for dependency in dependencies:
            self.parse_dependency(dependency, namespaces, m_dependencies)
        return m_dependencies

    def parse_dependency(self, dependency, namespaces, dependencies: list):
        dependency_id = dependency.attrib["{" + namespaces['xmi'] + "}" + "id"]
        dependency_source = dependency.attrib["supplier"]
        dependency_target = dependency.attrib["client"]
        dependency_type = "Dependency"
        dependency_rel = PckgRelation(dependency_id, dependency_source, dependency_target, dependency_type)
        dependencies.append(dependency_rel)
        return

    def parse_merges(self, packages, namespaces):
        m_merges = []
        for package in packages:
            self.parse_merge(package, namespaces, m_merges)
        return m_merges

    def parse_merge(self, package, namespaces, merges: list):
        children = package.getchildren()
        for child in children:
            if child.attrib["{" + namespaces['xmi'] + "}" + "type"] == "uml:PackageMerge":
                merge_id = child.attrib["{" + namespaces['xmi'] + "}" + "id"]
                merge_source = child.attrib["mergedPackage"]
                merge_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
                merge_type = "PackageMerge"
                m_merge = PckgRelation(merge_id, merge_source, merge_target, merge_type)
                merges.append(m_merge)
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
                import_source = child.attrib["importedPackage"]
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
            if child.attrib["{" + namespaces['xmi'] + "}" + "type"] == "uml:Package":
                # need to generate unique id
                member_id = str(uuid.uuid4())
                member_target = child.attrib["{" + namespaces['xmi'] + "}" + "id"]
                member_source = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
                member_type = "MemberOf"
                m_member = PckgRelation(member_id, member_source, member_target, member_type)
                members.append(m_member)
        return

    def parse_usages(self, model, namespaces):
        m_usage = []
        usages = model.findall('.//packagedElement[@xmi:type="uml:Usage"]', namespaces)
        for usage in usages:
            self.parse_usage(usage, namespaces, m_usage)
        return m_usage

    def parse_usage(self, usage, namespaces, usages):
        usage_id = usage.attrib["{" + namespaces['xmi'] + "}" + "id"]
        usage_source = usage.attrib["supplier"]
        usage_target = usage.attrib["client"]
        rel_type = "Usage"
        usage_rel = PckgRelation(usage_id, usage_source, usage_target, rel_type)
        usages.append(usage_rel)
        return

    def get_model(self, file_name, namespaces):
        return etree.parse(file_name).getroot().find('uml:Model', namespaces)

    def get_packages(self, model, namespaces):
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        return packages
