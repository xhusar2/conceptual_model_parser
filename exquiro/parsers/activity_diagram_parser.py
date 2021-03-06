from exquiro.models.activity_diagram.activity_diagram_model import ActivityDiagramModel
from exquiro.parsers.diagram_parser import DiagramParser
from lxml import etree


class ActivityDiagramParser(DiagramParser):
    def parse_file(self, file_name) -> ActivityDiagramModel:
        namespaces = self.get_namespaces(file_name)
        model = self.get_model(file_name, namespaces)
        return self.parse_model(model, namespaces)

    def parse_model(self, model, namespaces):
        model_id = self.parse_id(model, namespaces)
        nodes = self.parse_nodes(model, namespaces)
        relations = self.parse_relations(model, namespaces)
        return ActivityDiagramModel(model_id, nodes, relations)

    def parse_id(self, model, namespaces):
        pass

    def get_model(self, file_name, namespaces):
        pass

    def parse_nodes(self, model, namespaces):
        pass

    def parse_relations(self, model, namespaces):
        pass

    def parse_actions(self, model, namespaces):
        pass

    def parse_initial_nodes(self, model, namespaces):
        pass

    def parse_activity_finals(self, model, namespaces):
        pass

    def parse_flow_finals(self, model, namespaces):
        pass

    def parse_forks_joins(self, model, namespaces):
        pass

    def parse_decisions_merges(self, model, namespaces):
        pass

    def parse_control_flows(self, model, namespaces):
        pass

    def parse_object_flows(self, model, namespaces):
        pass

    def parse_partitions(self, model, namespaces):
        pass

    def parse_partition_relations(self, model, namespaces):
        pass

    def parse_central_buffers(self, model, namespaces):
        pass

    def parse_pins(self, model, namespaces):
        pass

    def parse_data_stores(self, model, namespaces):
        pass

    @staticmethod
    def get_namespaces(file_name):
        return etree.parse(file_name).getroot().nsmap
