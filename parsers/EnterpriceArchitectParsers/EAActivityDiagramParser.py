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
    def parse_node(node, namespaces, n_type, m_nodes):
        node_id = node.attrib["{" + namespaces['xmi'] + "}" + "id"]
        node_name = node.attrib["name"]
        node_type = n_type
        node_visibility = node.attrib["visibility"]
        node = ActivityNode(name=node_name, node_id=node_id, node_type=node_type, visibility=node_visibility)
        m_nodes.append(node)
        return

    def parse_actions(self, model, namespaces):
        m_actions = []
        actions = model.findall('.//node[@xmi:type="uml:Action"]', namespaces)
        for action in actions:
            self.parse_node(action, namespaces, "Action", m_actions)
        return m_actions

    def parse_initial_nodes(self, model, namespaces):
        m_initials = []
        initials = model.findall('.//node[@xmi:type="uml:InitialNode"]', namespaces)
        for initial in initials:
            self.parse_node(initial, namespaces, "Initial", m_initials)
        return m_initials

    def parse_activity_finals(self, model, namespaces):
        m_finals = []
        finals = model.findall('.//node[@xmi:type="uml:ActivityFinalNode"]', namespaces)
        for final in finals:
            self.parse_node(final, namespaces, "ActivityFinal", m_finals)
        return m_finals

    def parse_flow_finals(self, model, namespaces):
        m_flow_finals = []
        f_finals = model.findall('.//node[@xmi:type="uml:FlowFinalNode"]', namespaces)
        for f_final in f_finals:
            self.parse_node(f_final, namespaces, "FlowFinal", m_flow_finals)
        return m_flow_finals

    def parse_forks_joins(self, model, namespaces):
        m_forks = []
        forks = model.findall('.//node[@xmi:type="uml:ForkNode"]', namespaces)
        for fork in forks:
            self.parse_fork_join(fork, namespaces, m_forks)
        return m_forks

    @staticmethod
    def parse_fork_join(fork, namespaces, forks):
        node_id = fork.attrib["{" + namespaces['xmi'] + "}" + "id"]
        node_class = "ForkJoin"
        node_visibility = fork.attrib["visibility"]
        node = ActivityNode(node_id=node_id, node_type=node_class, visibility=node_visibility)
        forks.append(node)
        return

    def parse_decisions_merges(self, model, namespaces):
        m_decisions = []
        decisions = model.findall('.//node[@xmi:type="uml:DecisionNode"]', namespaces)
        for decision in decisions:
            self.parse_node(decision, namespaces, "DecisionMerge", m_decisions)
        return m_decisions

    def parse_central_buffers(self, model, namespaces):
        m_buffer = []
        buffers = model.findall('.//node[@xmi:type="uml:CentralBufferNode"]', namespaces)
        for buffer in buffers:
            self.parse_node(buffer, namespaces, "CentralBuffer", m_buffer)
        return m_buffer

    def parse_control_flows(self, model, namespaces):
        m_control_flows = []
        c_flows = model.findall('.//edge[@xmi:type="uml:ControlFlow"]', namespaces)
        for c_flow in c_flows:
            self.parse_control_flow(c_flow, namespaces, m_control_flows)
        return m_control_flows

    @staticmethod
    def parse_control_flow(c_flow, namespaces, c_flows):
        relation_id = c_flow.attrib["{" + namespaces['xmi'] + "}" + "id"]
        relation_source = c_flow.attrib["target"]
        relation_target = c_flow.attrib["source"]
        relation_type = "ControlFlow"
        relation_rel = ActivityRelation(relation_id, relation_source, relation_target, relation_type)
        c_flows.append(relation_rel)
        return

    def parse_object_flows(self, model, namespaces):
        m_object_flows = []
        o_flows = model.findall('.//edge[@xmi:type="uml:ObjectFlow"]', namespaces)
        for o_flow in o_flows:
            self.parse_object_flow(o_flow, namespaces, m_object_flows)
        return m_object_flows

    @staticmethod
    def parse_object_flow(o_flow, namespaces, o_flows):
        relation_id = o_flow.attrib["{" + namespaces['xmi'] + "}" + "id"]
        relation_source = o_flow.attrib["target"]
        relation_target = o_flow.attrib["source"]
        relation_type = "ObjectFlow"
        relation_rel = ActivityRelation(relation_id, relation_source, relation_target, relation_type)
        o_flows.append(relation_rel)
        return

    def parse_partitions(self, model, namespaces):
        m_partitions = []
        partitions = model.findall('.//group[@xmi:type="uml:ActivityPartition"]', namespaces)
        for partition in partitions:
            self.parse_partition(partition, namespaces, m_partitions)
        return m_partitions

    @staticmethod
    def parse_partition(partition, namespaces, partitions):
        node_id = partition.attrib["{" + namespaces['xmi'] + "}" + "id"]
        node_name = partition.attrib["name"]
        node_class = "Partition"
        node_visibility = partition.attrib["visibility"]
        node = ActivityNode(name=node_name, node_id=node_id, node_type=node_class, visibility=node_visibility)
        partitions.append(node)
        return

    def parse_partition_relations(self, model, namespaces):
        m_partition_rels = []
        partitions = model.findall('.//group[@xmi:type="uml:ActivityPartition"]', namespaces)
        for partition in partitions:
            self.parse_partition_relation(partition, namespaces, m_partition_rels)
        return m_partition_rels

    @staticmethod
    def parse_partition_relation(partition, namespaces, partition_relations):
        children = partition.getchildren()
        for child in children:
            # need to generate unique id
            rel_id = str(uuid.uuid4())
            rel_target = child.attrib["{" + namespaces['xmi'] + "}" + "idref"]
            rel_source = partition.attrib["{" + namespaces['xmi'] + "}" + "id"]
            rel_type = "PartitionMember"
            m_rel = ActivityRelation(rel_id, rel_source, rel_target, rel_type)
            partition_relations.append(m_rel)
        return

    def parse_pins(self, model, namespaces):
        m_pins = []
        self.parse_input_pins(model, namespaces, m_pins)
        self.parse_output_pins(model, namespaces, m_pins)
        return m_pins

    def parse_input_pins(self, model, namespaces, m_pins):
        input_pins = model.findall('.//input[@xmi:type="uml:InputPin"]', namespaces)
        for pin in input_pins:
            self.parse_pin(pin, namespaces, "InputPin", m_pins)
        return

    def parse_output_pins(self, model, namespaces, m_pins):
        input_pins = model.findall('.//output[@xmi:type="uml:OutputPin"]', namespaces)
        for pin in input_pins:
            self.parse_pin(pin, namespaces, "OutputPin", m_pins)
        return

    @staticmethod
    def parse_pin(pin, namespaces, p_type, m_pins):
        pin_id = pin.attrib["{" + namespaces['xmi'] + "}" + "id"]
        pin_name = pin.attrib["name"]
        pin_type = p_type
        pin_visibility = pin.attrib["visibility"]
        pin_ordering = pin.attrib["ordering"]
        node = ActivityNode(name=pin_name, node_id=pin_id, node_type=pin_type, visibility=pin_visibility, ordering=pin_ordering)
        m_pins.append(node)
        return

    def parse_instance_specifications(self, model, namespaces):
        m_objects = []
        instance_specifications = model.findall('.//packagedElement[@xmi:type="uml:InstanceSpecification"]', namespaces)
        for instance in instance_specifications:
            self.parse_node(instance, namespaces, "Object", m_objects)
        return m_objects

    def parse_datastores(self, model, namespaces):
        m_datastores = []
        datastores = model.findall('.//node[@xmi:type="uml:DataStoreNode"]', namespaces)
        for datastore in datastores:
            self.parse_node(datastore, namespaces, "DataStore", m_datastores)
        return m_datastores

    @staticmethod
    def parse_pin_relations(model, namespaces):
        pin_relations = []
        actions = model.findall('.//node[@xmi:type="uml:Action"]', namespaces)
        for action in actions:
            pins = action.findall('.//input[@xmi:type="uml:InputPin"]', namespaces)
            pins.extend(action.findall('.//output[@xmi:type="uml:OutputPin"]', namespaces))
            for pin in pins:
                rel_id = str(uuid.uuid4())
                rel_target = action.attrib["{" + namespaces['xmi'] + "}" + "id"]
                rel_source = pin.attrib["{" + namespaces['xmi'] + "}" + "id"]
                rel_type = "HasPin"
                m_rel = ActivityRelation(rel_id, rel_source, rel_target, rel_type)
                pin_relations.append(m_rel)
        return pin_relations
