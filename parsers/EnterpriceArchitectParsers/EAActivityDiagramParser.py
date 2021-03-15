from parsers.ActivityDiagramParser import ActivityDiagramParser
from models.activityDiagram.ActivityNode import ActivityNode
from models.activityDiagram.ActivityRelation import ActivityRelation
from lxml import etree
import uuid


class EAActDiagramParser(ActivityDiagramParser):
    def parse_id(self, model, namespaces):
        packaged_element = model.find('./packagedElement', namespaces)
        if packaged_element is not None:
            return packaged_element.attrib['{' + namespaces['xmi'] + '}' + 'id']
        id_attrib = '{' + namespaces['xmi'] + '}' + ':id'
        if id_attrib in model.attrib:
            return model.attrib[id_attrib]
        return ""

    def get_model(self, file_name, namespaces):
        return etree.parse(file_name).getroot().find('uml:Model', namespaces)

    def parse_nodes(self, model, namespaces):
        m_nodes = self.parse_actions(model, namespaces)
        m_nodes.extend(self.parse_activity_finals(model, namespaces))
        m_nodes.extend(self.parse_initial_nodes(model, namespaces))
        m_nodes.extend(self.parse_forks_joins(model, namespaces))
        m_nodes.extend(self.parse_flow_finals(model, namespaces))
        m_nodes.extend(self.parse_decisions_merges(model, namespaces))
        m_nodes.extend(self.parse_partitions(model, namespaces))
        m_nodes.extend(self.parse_central_buffers(model, namespaces))
        m_nodes.extend(self.parse_pins(model, namespaces))
        m_nodes.extend(self.parse_instance_specifications(model, namespaces))
        m_nodes.extend(self.parse_datastores(model, namespaces))
        return m_nodes

    def parse_relations(self, model, namespaces):
        m_relations = self.parse_control_flows(model, namespaces)
        m_relations.extend(self.parse_object_flows(model, namespaces))
        m_relations.extend(self.parse_partition_relations(model, namespaces))
        m_relations.extend(self.parse_pin_relations(model, namespaces))
        return m_relations

    # TODO rename
    @staticmethod
    def parse_node(node, namespaces, n_type):
        node_id = node.attrib["{" + namespaces['xmi'] + "}" + "id"]
        if 'name' in node.attrib:
            node_name = node.attrib["name"]
        else:
            node_name = None
        node_type = n_type
        node_visibility = node.attrib["visibility"]
        return ActivityNode(name=node_name, node_id=node_id, node_type=node_type, visibility=node_visibility)

    def parse_actions(self, model, namespaces):
        m_actions = []
        actions = model.findall('.//node[@xmi:type="uml:Action"]', namespaces)
        for action in actions:
            m_actions.append(self.parse_node(action, namespaces, "Action"))
        return m_actions

    def parse_initial_nodes(self, model, namespaces):
        m_initials = []
        initials = model.findall('.//node[@xmi:type="uml:InitialNode"]', namespaces)
        for initial in initials:
            m_initials.append(self.parse_node(initial, namespaces, "Initial"))
        return m_initials

    def parse_activity_finals(self, model, namespaces):
        m_finals = []
        finals = model.findall('.//node[@xmi:type="uml:ActivityFinalNode"]', namespaces)
        for final in finals:
            m_finals.append(self.parse_node(final, namespaces, "ActivityFinal"))
        return m_finals

    def parse_flow_finals(self, model, namespaces):
        m_flow_finals = []
        f_finals = model.findall('.//node[@xmi:type="uml:FlowFinalNode"]', namespaces)
        for f_final in f_finals:
            m_flow_finals.append(self.parse_node(f_final, namespaces, "FlowFinal"))
        return m_flow_finals

    def parse_forks_joins(self, model, namespaces):
        m_forks = []
        forks = model.findall('.//node[@xmi:type="uml:ForkNode"]', namespaces)
        for fork in forks:
            m_forks.append(self.parse_node(fork, namespaces, "ForkJoin"))
        return m_forks

    def parse_decisions_merges(self, model, namespaces):
        m_decisions = []
        decisions = model.findall('.//node[@xmi:type="uml:DecisionNode"]', namespaces)
        for decision in decisions:
            m_decisions.append(self.parse_node(decision, namespaces, "DecisionMerge"))
        return m_decisions

    def parse_central_buffers(self, model, namespaces):
        m_buffer = []
        buffers = model.findall('.//node[@xmi:type="uml:CentralBufferNode"]', namespaces)
        for buffer in buffers:
            m_buffer.append(self.parse_node(buffer, namespaces, "CentralBuffer"))
        return m_buffer

    @staticmethod
    def parse_flow_relation(flow, namespaces, rel_type):
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

    def parse_control_flows(self, model, namespaces):
        m_control_flows = []
        c_flows = model.findall('.//edge[@xmi:type="uml:ControlFlow"]', namespaces)
        for c_flow in c_flows:
            m_control_flows.append(self.parse_flow_relation(c_flow, namespaces, "ControlFlow"))
        return m_control_flows

    def parse_object_flows(self, model, namespaces):
        m_object_flows = []
        o_flows = model.findall('.//edge[@xmi:type="uml:ObjectFlow"]', namespaces)
        for o_flow in o_flows:
            m_object_flows.append(self.parse_flow_relation(o_flow, namespaces, "ObjectFlow"))
        return m_object_flows

    def parse_partitions(self, model, namespaces):
        m_partitions = []
        partitions = model.findall('.//group[@xmi:type="uml:ActivityPartition"]', namespaces)
        for partition in partitions:
            m_partitions.append(self.parse_node(partition, namespaces, "Partition"))
        return m_partitions

    def parse_partition_relations(self, model, namespaces):
        m_partition_relations = []
        partitions = model.findall('.//group[@xmi:type="uml:ActivityPartition"]', namespaces)
        for partition in partitions:
            children = partition.getchildren()
            for child in children:
                m_partition_relations.append(self.parse_partition_relation(child, partition, namespaces))
        return m_partition_relations

    @staticmethod
    def parse_partition_relation(child, partition, namespaces):
        # need to generate unique id
        rel_id = str(uuid.uuid4())
        rel_source = child.attrib["{" + namespaces['xmi'] + "}" + "idref"]
        rel_target = partition.attrib["{" + namespaces['xmi'] + "}" + "id"]
        rel_type = "PartitionMember"
        return ActivityRelation(rel_id, rel_source, rel_target, rel_type)

    def parse_pins(self, model, namespaces):
        m_pins = []
        m_pins.extend(self.parse_input_pins(model, namespaces))
        m_pins.extend(self.parse_output_pins(model, namespaces))
        return m_pins

    def parse_input_pins(self, model, namespaces):
        m_input_pins = []
        input_pins = model.findall('.//input[@xmi:type="uml:InputPin"]', namespaces)
        for pin in input_pins:
            m_input_pins.append(self.parse_pin(pin, namespaces, "InputPin"))
        return m_input_pins

    def parse_output_pins(self, model, namespaces):
        m_output_pins = []
        output_pins = model.findall('.//output[@xmi:type="uml:OutputPin"]', namespaces)
        for pin in output_pins:
            m_output_pins.append(self.parse_pin(pin, namespaces, "OutputPin"))
        return m_output_pins

    @staticmethod
    def parse_pin(pin, namespaces, p_type):
        pin_id = pin.attrib["{" + namespaces['xmi'] + "}" + "id"]
        pin_name = pin.attrib["name"]
        pin_type = p_type
        pin_visibility = pin.attrib["visibility"]
        pin_ordering = pin.attrib["ordering"]
        return ActivityNode(name=pin_name, node_id=pin_id, node_type=pin_type, visibility=pin_visibility, ordering=pin_ordering)

    def parse_instance_specifications(self, model, namespaces):
        m_objects = []
        instance_specifications = model.findall('.//packagedElement[@xmi:type="uml:InstanceSpecification"]', namespaces)
        for instance in instance_specifications:
            m_objects.append(self.parse_node(instance, namespaces, "Object"))
        return m_objects

    def parse_data_stores(self, model, namespaces):
        m_data_stores = []
        data_stores = model.findall('.//node[@xmi:type="uml:DataStoreNode"]', namespaces)
        for data_store in data_stores:
            m_data_stores.append(self.parse_node(data_store, namespaces, "DataStore"))
        return m_data_stores

    @staticmethod
    def parse_pin_relations(model, namespaces):
        pin_relations = []
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
                pin_relations.append(m_rel)
        return pin_relations
