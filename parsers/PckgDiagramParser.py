from models.packageDiagram.PckgDiagramModel import PackageDiagramModel
from lxml import etree


class PckgDiagramParser:

    def parse_file(self, file_name: str) -> PackageDiagramModel:
        namespaces = self.get_namespaces(file_name)
        model = self.get_model(file_name, namespaces)
        return self.parse_model(model, namespaces)

    def parse_model(self, model, namespaces):
        m_id = self.parse_id(model, namespaces)
        m_nodes = self.parse_nodes(model, namespaces)
        m_relations = self.parse_relations(model, namespaces)
        return PackageDiagramModel(m_id, m_nodes, m_relations)

    def parse_nodes(self, model, namespaces):
        pass

    def parse_relations(self, model, namespaces):
        pass

    def parse_id(self, model, namespaces):
        pass

    def parse_packages(self, model, namespaces):
        pass

    def parse_package(self, package, namespaces, packages):
        pass

    def parse_dependencies(self, model, namespaces):
        pass

    def parse_dependency(self, dependency, namespaces, dependencies):
        pass

    def parse_merges(self, packages, namespaces):
        pass

    def parse_merge(self, package, namespaces, merges):
        pass

    def parse_imports(self, packages, namespaces):
        pass

    def parse_import(self, package, namespaces, imports):
        pass

    def parse_member_packages(self, packages, namespaces):
        pass

    def parse_member_package(self, package, namespaces, members):
        pass

    def parse_usages(self, packages, namespaces):
        pass

    def parse_usage(self, model, namespaces, usages):
        pass

    def get_model(self, file_name, namespaces):
        pass

    @staticmethod
    def get_namespaces(file_name):
        return etree.parse(file_name).getroot().nsmap
