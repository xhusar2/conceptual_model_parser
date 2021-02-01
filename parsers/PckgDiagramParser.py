from models.packageDiagram.PckgDiagramModel import PackageDiagramModel
from lxml import etree


class PckgDiagramParser:

    def parse_file(self, file_name: str) -> PackageDiagramModel:
        namespaces = self.get_namespaces(file_name)
        model = self.get_model(file_name, namespaces)
        return self.parse_model(model, namespaces)

    def parse_model(self, model, namespaces):
        m_id = self.parse_id(model, namespaces)
        m_classes = self.parse_packages(model, namespaces)
        m_relations = self.parse_dependencies(model, namespaces)
        return PackageDiagramModel(m_id, m_classes, m_relations)

    def parse_id(self, model, namespaces):
        pass

    def parse_packages(self, model, namespaces):
        pass

    def parse_package(self, p, namespaces, packages):
        pass

    def parse_dependencies(self, model, namespaces):
        pass

    def parse_dependency(self, d, namespaces, dependencies):
        pass

    @staticmethod
    def get_model(file_name, namespaces):
        return etree.parse(file_name).find('uml:Model', namespaces)

    @staticmethod
    def get_namespaces(file_name):
        return etree.parse(file_name).getroot().nsmap
