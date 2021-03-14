from parsers.PackageDiagramParser import PackageDiagramParser
from models.packageDiagram.PackageNode import PackageNode
from models.packageDiagram.PackageRelation import PackageRelation
from lxml import etree
import uuid


class VPPackageParser(PackageDiagramParser):
    def parse_nodes(self, model, namespaces):
        m_nodes = self.parse_packages(model, namespaces)
        return m_nodes

    def parse_relations(self, model, namespaces):
        m_relations = self.parse_dependencies(model, namespaces)
        m_relations.extend(self.parse_imports(model, namespaces))
        m_relations.extend(self.parse_merges(model, namespaces))
        m_relations.extend(self.parse_member_packages(self.get_packages(model, namespaces), namespaces))
        return m_relations

    def parse_id(self, model, namespaces):
        pass

    def parse_packages(self, model, namespaces):
        m_packages = []
        packages = self.get_packages(model, namespaces)
        for package in packages:
            self.parse_package(package, namespaces, m_packages)
        return m_packages

    def parse_package(self, package, namespaces, packages):
        node_id = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
        node_name = package.attrib["name"]
        node_class = "Package"
        if 'visibility' in package.attrib:
            node_visibility = package.attrib["visibility"]
        else:
            node_visibility = "public"
        node = PackageNode(node_name, node_id, node_class, node_visibility)
        packages.append(node)
        return

    def parse_dependencies(self, model, namespaces):
        m_dependencies = []
        dependencies = model.findall('.//ownedMember[@xmi:type="uml:Dependency"]', namespaces)
        for dependency in dependencies:
            self.parse_dependency(dependency, namespaces, m_dependencies)
        return m_dependencies

    def parse_dependency(self, dependency, namespaces, dependencies):
        dependency_id = dependency.attrib["{" + namespaces['xmi'] + "}" + "id"]
        dependency_target = dependency.attrib["supplier"]
        dependency_source = dependency.attrib["client"]
        dependency_type = "Dependency"
        dependency_rel = PackageRelation(dependency_id, dependency_source, dependency_target, dependency_type)
        dependencies.append(dependency_rel)
        return

    def parse_merges(self, model, namespaces):
        m_merge = []
        merges = model.findall('.//packageMerge', namespaces)
        for merge in merges:
            self.parse_merge(merge, namespaces, m_merge)
        return m_merge

    def parse_merge(self, merge, namespaces, merges):
        merge_id = merge.attrib["{" + namespaces['xmi'] + "}" + "id"]
        merge_target = merge.attrib["supplier"]
        merge_source = merge.attrib["client"]
        merge_type = "PackageMerge"
        m_merge = PackageRelation(merge_id, merge_source, merge_target, merge_type)
        merges.append(m_merge)
        return

    def parse_imports(self, model, namespaces):
        m_imports = []
        imports = model.findall('.//packageImport', namespaces)
        for import_e in imports:
            self.parse_import(import_e, namespaces, m_imports)
        return m_imports

    def parse_import(self, import_e, namespaces, imports):
        import_id = import_e.attrib["{" + namespaces['xmi'] + "}" + "id"]
        import_target = import_e.attrib["supplier"]
        import_source = import_e.attrib["client"]
        applied_stereotype = import_e.find('.//appliedStereotype', namespaces)
        if applied_stereotype.attrib["{" + namespaces['xmi'] + "}" + "value"] == "Dependency_import_id":
            import_type = "PackageImport"
        else:
            import_type = "PackageAccess"
        m_import = PackageRelation(import_id, import_source, import_target, import_type)
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
            if self.is_package(child, namespaces):
                # need to generate unique id
                member_id = str(uuid.uuid4())
                member_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
                member_source = child.attrib["{" + namespaces['xmi'] + "}" + "id"]
                member_type = "MemberOf"
                m_member = PackageRelation(member_id, member_source, member_target, member_type)
                members.append(m_member)
        return

    def get_model(self, file_name, namespaces):
        return etree.parse(file_name).getroot().find('uml:Model', namespaces)

    @staticmethod
    def get_packages(model, namespaces):
        packages = model.findall('.//ownedMember[@xmi:type="uml:Package"]', namespaces)
        packages.extend(model.findall('.//ownedMember[@xmi:type="uml:Component"]', namespaces))
        packages.extend(model.findall('.//ownedMember[@xmi:type="uml:Model"]', namespaces))
        return packages

    @staticmethod
    def is_package(element, namespaces):
        if "{" + namespaces['xmi'] + "}" + "type" not in element.attrib:
            return False
        el_type = element.attrib["{" + namespaces['xmi'] + "}" + "type"]
        return el_type == "uml:Package" or el_type == "uml:Model" or el_type == "uml:Component"
