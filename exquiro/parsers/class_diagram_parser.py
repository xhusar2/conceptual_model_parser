from lxml import etree
from ..models.class_diagram.class_diagram_model import ClsDiagramModel

class ClsDiagramParser:
    """ Parser should take file with XMI model and return model ready to be inserted to Neo4j (nodes and
    relationships) """

    # Input: xmi/xml file
    # Output parsed model ready to be stored to Neo4j
    def parse_file(self, file_name: str) -> ClsDiagramModel:
        namespaces = self.get_namespaces(file_name)
        model = self.get_model(file_name, namespaces)
        return self.parse_model(model, namespaces)

    def parse_model(self, model, namespaces):
        m_id = self.parse_id(model, namespaces)
        m_classes = self.parse_classes(model, namespaces)
        m_associations, m_association_nodes = self.parse_associations(model, namespaces)
        m_generalizations = self.parse_generalizations(model, namespaces)
        c_types, a_types = self.parse_types(model, namespaces)
        m_gsets = self.parse_generalization_sets(model, namespaces)
        # TODO return neo4j model consisting from nodes and relations only
        #  implement in ClsDiagramModel
        return ClsDiagramModel(m_id, m_classes, m_associations, m_association_nodes
                               , m_generalizations, m_gsets, c_types, a_types)

    def parse_id(self, model, namespaces):
        pass

    def parse_classes(self, model, namespaces):
        pass

    def parse_types(self, model, namespaces):
        pass

    def parse_generalization_sets(self, model, namespaces):
        pass

    def parse_gset(self, gs, namespaces):
        pass

    def parse_class(self, c, namespaces):
        pass

    def parse_generalizations(self, model, namespaces):
        pass

    def parse_attributes(self, c, namespaces):
        pass

    def parse_association(self, a, model, namespaces):
        # parses association based on specific model format, implemented in format specific model class
        pass

    def parse_owned_ends(self, a, namespaces):
        # parses association based on specific model format, implemented in format specific model class
        pass

    def parse_generalization(self, cls, namespaces):
        pass

    def parse_attribute(self, attribute, namespaces):
        pass

    def get_model(self, file_name, namespaces):
        return etree.parse(file_name).find('uml:Model', namespaces)

    def get_namespaces(self, file_name):
        return etree.parse(file_name).getroot().nsmap

    def get_root(self, file_name):
        self.root = etree.parse(file_name).getroot()
        return self.root

    def parse_associations(self, model, namespace):
        pass

    def find_ref_element(self, model, id_ref, namespaces):
        pass
