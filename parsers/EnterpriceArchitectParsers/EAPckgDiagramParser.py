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

    # TODO refactor
    def parse_packages(self, model, namespaces):
        m_packages = []
        packages = model.findall('.//packagedElement[@xmi:type="uml:Package"]', namespaces)
        # skip first package it is package of the whole diagram
        packages = packages[1:]
        for p in packages:
            self.parse_package(p, namespaces, m_packages)
        return m_packages

    # TODO refactor
    def parse_package(self, p, namespaces, packages: list):
        # new node
        node_id = p.attrib["{" + namespaces['xmi'] + "}" + "id"]
        n = PckgNode(p.attrib["name"], node_id, "uml:Package")
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
        d_type = "Dependency"
        m_d = PckgRelation(d_id, d_source, d_target, d_type)
        dependencies.append(m_d)
        return
