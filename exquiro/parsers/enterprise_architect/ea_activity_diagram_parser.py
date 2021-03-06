from exquiro.parsers.activity_diagram_parser import ActivityDiagramParser
from exquiro.models.activity_diagram.activity_node import ActivityNode
from exquiro.models.activity_diagram.activity_relation import ActivityRelation
from lxml import etree
import uuid


class EAActivityDiagramParser(ActivityDiagramParser):
    def parse_id(self, model, namespaces):
        return str(uuid.uuid4())

    def get_model(self, file_name, namespaces):
        return etree.parse(file_name).getroot().find('uml:Model', namespaces)

    def parse_nodes(self, model, namespaces):
        try:
            nodes = self.parse_actions(model, namespaces)
            nodes.update(self.parse_activity_finals(model, namespaces))
            nodes.update(self.parse_initial_nodes(model, namespaces))
            nodes.update(self.parse_forks_joins(model, namespaces))
            nodes.update(self.parse_flow_finals(model, namespaces))
            nodes.update(self.parse_decisions_merges(model, namespaces))
            nodes.update(self.parse_partitions(model, namespaces))
            nodes.update(self.parse_central_buffers(model, namespaces))
            nodes.update(self.parse_pins(model, namespaces))
            nodes.update(self.parse_data_stores(model, namespaces))
            return nodes
        except AttributeError as exc:
            raise exc
        except Exception as exc:
            raise Exception("Corrupted model in source file") from exc

    def parse_relations(self, model, namespaces):
        try:
            relations = self.parse_control_flows(model, namespaces)
            relations.update(self.parse_object_flows(model, namespaces))
            relations.update(self.parse_partition_relations(model, namespaces))
            relations.update(self.parse_pin_relations(model, namespaces))
            return relations
        except AttributeError as exc:
            raise exc
        except Exception as exc:
            raise Exception("Corrupted model in source file") from exc

    @staticmethod
    def parse_activity_node(node, namespaces, n_type):
        try:
            node_id = node.attrib["{" + namespaces['xmi'] + "}" + "id"]
            if 'name' in node.attrib and node.attrib['name'] is not "":
                node_name = node.attrib["name"]
            else:
                node_name = None
            if 'ordering' in node.attrib:
                node_ordering = node.attrib["ordering"]
            else:
                node_ordering = None
            node_type = n_type
            node_visibility = node.attrib["visibility"]
            return ActivityNode(name=node_name, node_id=node_id, node_type=node_type, visibility=node_visibility,
                                ordering=node_ordering)
        except Exception as exc:
            raise AttributeError("Corrupted activity node in source file: type " + n_type) from exc

    def parse_actions(self, model, namespaces):
        m_actions = set()
        actions = model.findall('.//node[@xmi:type="uml:Action"]', namespaces)
        for action in actions:
            m_actions.add(self.parse_activity_node(action, namespaces, "Action"))
        return m_actions

    def parse_initial_nodes(self, model, namespaces):
        m_initials = set()
        initials = model.findall('.//node[@xmi:type="uml:InitialNode"]', namespaces)
        for initial in initials:
            m_initials.add(self.parse_activity_node(initial, namespaces, "Initial"))
        return m_initials

    def parse_activity_finals(self, model, namespaces):
        m_finals = set()
        finals = model.findall('.//node[@xmi:type="uml:ActivityFinalNode"]', namespaces)
        for final in finals:
            m_finals.add(self.parse_activity_node(final, namespaces, "ActivityFinal"))
        return m_finals

    def parse_flow_finals(self, model, namespaces):
        m_flow_finals = set()
        f_finals = model.findall('.//node[@xmi:type="uml:FlowFinalNode"]', namespaces)
        for f_final in f_finals:
            m_flow_finals.add(self.parse_activity_node(f_final, namespaces, "FlowFinal"))
        return m_flow_finals

    def parse_forks_joins(self, model, namespaces):
        m_forks = set()
        forks = model.findall('.//node[@xmi:type="uml:ForkNode"]', namespaces)
        for fork in forks:
            m_forks.add(self.parse_activity_node(fork, namespaces, "ForkJoin"))
        return m_forks

    def parse_decisions_merges(self, model, namespaces):
        m_decisions = set()
        decisions = set(model.findall('.//node[@xmi:type="uml:DecisionNode"]', namespaces))
        decisions.update(model.findall('.//node[@xmi:type="uml:MergeNode"]', namespaces))
        for decision in decisions:
            m_decisions.add(self.parse_activity_node(decision, namespaces, "DecisionMerge"))
        return m_decisions

    def parse_central_buffers(self, model, namespaces):
        m_buffer = set()
        buffers = model.findall('.//node[@xmi:type="uml:CentralBufferNode"]', namespaces)
        for buffer in buffers:
            m_buffer.add(self.parse_activity_node(buffer, namespaces, "CentralBuffer"))
        return m_buffer

    @staticmethod
    def parse_flow_relation(flow, namespaces, rel_type):
        try:
            guard = flow.find('.//guard[@xmi:type="uml:OpaqueExpression"]', namespaces)
            if guard is not None and 'body' in guard.attrib:
                relation_guard = guard.attrib["body"]
            else:
                relation_guard = None
            relation_id = flow.attrib["{" + namespaces['xmi'] + "}" + "id"]
            relation_target = flow.attrib["target"]
            relation_source = flow.attrib["source"]
            relation_type = rel_type
            return ActivityRelation(relation_id, relation_source, relation_target, relation_type, relation_guard)
        except Exception as exc:
            raise AttributeError("Corrupted relation in source file: type " + rel_type) from exc

    def parse_control_flows(self, model, namespaces):
        m_control_flows = set()
        c_flows = model.findall('.//edge[@xmi:type="uml:ControlFlow"]', namespaces)
        for c_flow in c_flows:
            m_control_flows.add(self.parse_flow_relation(c_flow, namespaces, "ControlFlow"))
        return m_control_flows

    def parse_object_flows(self, model, namespaces):
        m_object_flows = set()
        o_flows = model.findall('.//edge[@xmi:type="uml:ObjectFlow"]', namespaces)
        for o_flow in o_flows:
            m_object_flows.add(self.parse_flow_relation(o_flow, namespaces, "ObjectFlow"))
        return m_object_flows

    def parse_partitions(self, model, namespaces):
        m_partitions = set()
        partitions = model.findall('.//group[@xmi:type="uml:ActivityPartition"]', namespaces)
        for partition in partitions:
            m_partitions.add(self.parse_activity_node(partition, namespaces, "Partition"))
        return m_partitions

    def parse_partition_relations(self, model, namespaces):
        m_partition_relations = set()
        partitions = model.findall('.//group[@xmi:type="uml:ActivityPartition"]', namespaces)
        for partition in partitions:
            partition_members = list(set(partition.getchildren()) & set(partition.findall('.//node')))
            for partition_member in partition_members:
                m_partition_relations.add(self.parse_partition_relation(partition_member, partition, namespaces))
        return m_partition_relations

    @staticmethod
    def parse_partition_relation(child, partition, namespaces):
        try:
            # need to generate unique id
            rel_id = str(uuid.uuid4())
            rel_source = child.attrib["{" + namespaces['xmi'] + "}" + "idref"]
            rel_target = partition.attrib["{" + namespaces['xmi'] + "}" + "id"]
            rel_type = "PartitionMember"
            return ActivityRelation(rel_id, rel_source, rel_target, rel_type)
        except Exception as exc:
            raise AttributeError("Corrupted partition or one of its member in source file") from exc

    def parse_pins(self, model, namespaces):
        m_pins = set()
        m_pins.update(self.parse_input_pins(model, namespaces))
        m_pins.update(self.parse_output_pins(model, namespaces))
        return m_pins

    def parse_input_pins(self, model, namespaces):
        m_input_pins = set()
        input_pins = model.findall('.//input[@xmi:type="uml:InputPin"]', namespaces)
        for pin in input_pins:
            m_input_pins.add(self.parse_activity_node(pin, namespaces, "InputPin"))
        return m_input_pins

    def parse_output_pins(self, model, namespaces):
        m_output_pins = set()
        output_pins = model.findall('.//output[@xmi:type="uml:OutputPin"]', namespaces)
        for pin in output_pins:
            m_output_pins.add(self.parse_activity_node(pin, namespaces, "OutputPin"))
        return m_output_pins

    def parse_data_stores(self, model, namespaces):
        m_data_stores = set()
        data_stores = model.findall('.//node[@xmi:type="uml:DataStoreNode"]', namespaces)
        for data_store in data_stores:
            m_data_stores.add(self.parse_activity_node(data_store, namespaces, "DataStore"))
        return m_data_stores

    @staticmethod
    def parse_pin_relations(model, namespaces):
        try:
            pin_relations = set()
            actions = model.findall('.//node[@xmi:type="uml:Action"]', namespaces)
            for action in actions:
                pins = action.findall('.//input[@xmi:type="uml:InputPin"]', namespaces)
                pins.extend(action.findall('.//output[@xmi:type="uml:OutputPin"]', namespaces))
                for pin in pins:
                    rel_id = str(uuid.uuid4())
                    rel_target = pin.attrib["{" + namespaces['xmi'] + "}" + "id"]
                    rel_source = action.attrib["{" + namespaces['xmi'] + "}" + "id"]
                    rel_type = "HasPin"
                    m_rel = ActivityRelation(rel_id, rel_source, rel_target, rel_type)
                    pin_relations.add(m_rel)
            return pin_relations
        except Exception as exc:
            raise AttributeError("Corrupted pin node or action node in source file") from exc