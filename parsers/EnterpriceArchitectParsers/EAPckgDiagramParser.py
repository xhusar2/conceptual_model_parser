from parsers.PckgDiagramParser import PckgDiagramParser
from models.packageDiagram.PckgNode import PckgNode
from models.packageDiagram.PckgRelation import PckgRelation


class EAPckgDiagramParser(PckgDiagramParser):

    # first packaged element in model is package of whole diagram
    # TODO refactor end
    def parse_id(self, model, namespaces):
        packaged_element = model.find('./packagedElement', namespaces)
        if packaged_element is not None:
            return packaged_element.attrib['{' + namespaces['xmi'] + '}' + 'id']
        id_attrib = '{' + namespaces['xmi'] + '}' + ':id'
        if id_attrib in model.attrib:
            return model.attrib[id_attrib]
        return ""

    # TODO refactor pass package not model to not slice package
    def parse_packages(self, model, namespaces):
        m_packages = []
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        # skip first package it is package of the whole diagram
        packages = packages[1:]
        for p in packages:
            self.parse_package(p, namespaces, m_packages)
        return m_packages

    def parse_package(self, p, namespaces, packages: list):
        node_id = p.attrib["{" + namespaces['xmi'] + "}" + "id"]
        n = PckgNode(p.attrib["name"], node_id, "uml:Package", p.attrib["visibility"])
        packages.append(n)
        return

    def parse_dependencies(self, model, namespaces):
        m_dependencies = []
        dependencies = model.findall('.//packagedElement[@xmi:type="uml:Dependency"]', namespaces)
        for d in dependencies:
            self.parse_dependency(d, namespaces, m_dependencies)
        return m_dependencies

    def parse_dependency(self, d, namespaces, dependencies: list):
        d_id = d.attrib["{" + namespaces['xmi'] + "}" + "id"]
        d_source = d.attrib["supplier"]
        d_target = d.attrib["client"]
        d_type = "dependencyRelation"
        m_d = PckgRelation(d_id, d_source, d_target, d_type)
        dependencies.append(m_d)
        return

    def parse_merges(self, model, namespaces):
        m_merges = []
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        packages = packages[1:]
        for p in packages:
            self.parse_merge(p, namespaces, m_merges)
        return m_merges

    def parse_merge(self, package, namespaces, merges):
        merge_elements = package.findall('.//packageMerge[@xmi:type="uml:PackageMerge"]', namespaces)
        for m in merge_elements:
            m_id = m.attrib["{" + namespaces['xmi'] + "}" + "id"]
            m_source = m.attrib["mergedPackage"]
            m_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
            m_type = "mergeRelation"
            m_m = PckgRelation(m_id, m_source, m_target, m_type)
            merges.append(m_m)
        return

    def parse_profiles(self, model, namespaces):
        m_profiles = []
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        packages = packages[1:]
        for p in packages:
            self.parse_profile(p, namespaces, m_profiles)
        return m_profiles

    def parse_profile(self, package, namespaces, profiles):
        profile_elements = package.findall('.//profileApplication[@xmi:type="uml:ProfileApplication"]', namespaces)
        for p in profile_elements:
            p_id = p.attrib["{" + namespaces['xmi'] + "}" + "id"]
            p_source = p.attrib["appliedProfile"]
            p_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
            p_type = "profileRelation"
            m_p = PckgRelation(p_id, p_source, p_target, p_type)
            profiles.append(m_p)
        return

    def parse_imports(self, model, namespaces):
        m_imports = []
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        packages = packages[1:]
        for p in packages:
            self.parse_import(p, namespaces, m_imports)
        return m_imports

    def parse_import(self, package, namespaces, imports):
        import_elements = package.findall('.//packageImport[@xmi:type="uml:PackageImport"]', namespaces)
        for i in import_elements:
            i_id = i.attrib["{" + namespaces['xmi'] + "}" + "id"]
            i_source = i.attrib["importedPackage"]
            i_target = package.attrib["{" + namespaces['xmi'] + "}" + "id"]
            i_type = "importRelation"
            m_p = PckgRelation(i_id, i_source, i_target, i_type)
            imports.append(m_p)
        return
