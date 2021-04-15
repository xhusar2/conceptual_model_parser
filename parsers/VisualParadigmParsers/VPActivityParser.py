from parsers.ActivityDiagramParser import ActivityDiagramParser
from models.activityDiagram.ActivityNode import ActivityNode
from models.activityDiagram.ActivityRelation import ActivityRelation
from lxml import etree
import uuid


class VPActivityParser(ActivityDiagramParser):
    def parse_id(self, model, namespaces):
        if '{' + namespaces['xmi'] + '}' + 'id' not in model.attrib:
            return uuid.uuid4()
        else:
            return model.attrib['{' + namespaces['xmi'] + '}' + 'id']

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
            relations.update(self.parse_partition_relations(model, namespaces))
            relations.update(self.parse_object_flows(model, namespaces))
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
            node_name = None
            if 'name' in node.attrib and node.attrib["name"] != "":
                node_name = node.attrib["name"]
            node_visibility = None
            if 'visibility' in node.attrib and node.attrib["visibility"] != "":
                node_visibility = node.attrib["visibility"]
            ordering = None
            if 'ordering' in node.attrib and node.attrib["ordering"] != "":
                ordering = node.attrib["ordering"]
            node_type = n_type
            return ActivityNode(name=node_name, node_id=node_id, node_type=node_type, visibility=node_visibility, ordering=ordering)
        except Exception as exc:
            raise AttributeError("Corrupted activity node in source file: type " + n_type) from exc

    def parse_actions(self, model, namespaces):
        m_actions = set()
        actions = set(model.findall('.//ownedMember[@xmi:type="uml:CallBehaviorAction"]', namespaces))
        actions.update(model.findall('.//node[@xmi:type="uml:CallBehaviorAction"]', namespaces))
        for action in actions:
            m_actions.add(self.parse_activity_node(action, namespaces, "Action"))
        return m_actions

    def parse_initial_nodes(self, model, namespaces):
        m_initial_nodes = set()
        initial_nodes = set(set(model.findall('.//ownedMember[@xmi:type="uml:Pseudostate"]', namespaces)) &
                            set(model.findall('.//ownedMember[@kind="initial"]')))
        initial_nodes.update(set(set(model.findall('.//node[@xmi:type="uml:Pseudostate"]', namespaces)) &
                             set(model.findall('.//node[@kind="initial"]'))))
        for initial in initial_nodes:
            m_initial_nodes.add(self.parse_activity_node(initial, namespaces, "Initial"))
        return m_initial_nodes

    def parse_activity_finals(self, model, namespaces):
        m_activity_finals = set()
        activity_finals = set(set(model.findall('.//ownedMember[@xmi:type="uml:Pseudostate"]', namespaces)) &
                              set(model.findall('.//ownedMember[@kind="final"]')))
        activity_finals.update(set(set(model.findall('.//node[@xmi:type="uml:Pseudostate"]', namespaces)) &
                               set(model.findall('.//node[@kind="final"]'))))
        for activity_final in activity_finals:
            final_type = activity_final.find('.//activityFinalNode', namespaces)
            if final_type is not None:
                m_activity_finals.add(self.parse_activity_node(activity_final, namespaces, "ActivityFinal"))
        return m_activity_finals

    def parse_flow_finals(self, model, namespaces):
        m_flow_finals = set()
        flow_finals = set(set(model.findall('.//ownedMember[@xmi:type="uml:Pseudostate"]', namespaces)) &
                          set(model.findall('.//ownedMember[@kind="final"]')))
        flow_finals.update(set(set(model.findall('.//node[@xmi:type="uml:Pseudostate"]', namespaces)) &
                           set(model.findall('.//node[@kind="final"]'))))
        for activity_final in flow_finals:
            final_type = activity_final.find('.//flowFinalNode', namespaces)
            if final_type is not None:
                m_flow_finals.add(self.parse_activity_node(activity_final, namespaces, "FlowFinal"))
        return m_flow_finals

    def parse_forks_joins(self, model, namespaces):
        m_forks_joins = set()
        forks_joins = set(set(model.findall('.//ownedMember[@xmi:type="uml:Pseudostate"]', namespaces)) &
                          set(model.findall('.//ownedMember[@kind="fork"]')))
        forks_joins.update(set(set(model.findall('.//node[@xmi:type="uml:Pseudostate"]', namespaces)) &
                           set(model.findall('.//node[@kind="fork"]'))))
        forks_joins.update(set(set(model.findall('.//ownedMember[@xmi:type="uml:Pseudostate"]', namespaces)) &
                               set(model.findall('.//ownedMember[@kind="join"]'))))
        forks_joins.update(set(set(model.findall('.//node[@xmi:type="uml:Pseudostate"]', namespaces)) &
                               set(model.findall('.//node[@kind="join"]'))))
        for fork_join in forks_joins:
            m_forks_joins.add(self.parse_activity_node(fork_join, namespaces, "ForkJoin"))
        return m_forks_joins

    def parse_decisions_merges(self, model, namespaces):
        m_decisions_merges = set()
        decisions_merges = set(set(model.findall('.//ownedMember[@xmi:type="uml:Pseudostate"]', namespaces)) &
                           set(model.findall('.//ownedMember[@kind="junction"]')))
        decisions_merges.update(set(set(model.findall('.//node[@xmi:type="uml:Pseudostate"]', namespaces)) &
                                set(model.findall('.//node[@kind="junction"]'))))
        for decision_merge in decisions_merges:
            m_decisions_merges.add(self.parse_activity_node(decision_merge, namespaces, "DecisionMerge"))
        return m_decisions_merges

    @staticmethod
    def parse_flow_relation(relation, namespaces, rel_type):
        try:
            relation_id = relation.attrib["{" + namespaces['xmi'] + "}" + "id"]
            relation_target = relation.attrib["target"]
            relation_source = relation.attrib["source"]
            relation_type = rel_type
            if 'name' in relation.attrib and relation.attrib["name"] != "":
                relation_guard = relation.attrib["name"]
            else:
                relation_guard = None
            return ActivityRelation(relation_id, relation_source, relation_target, relation_type, relation_guard)
        except Exception as exc:
            raise AttributeError("Corrupted activity edge in source file: type " + rel_type) from exc

    def parse_control_flows(self, model, namespaces):
        m_control_flows = set()
        control_flows = model.findall('.//edge[@xmi:type="uml:ControlFlow"]', namespaces)
        for control_flow in control_flows:
            m_control_flows.add(self.parse_flow_relation(control_flow, namespaces, "ControlFlow"))
        return m_control_flows

    def parse_object_flows(self, model, namespaces):
        m_object_flows = set()
        object_flows = model.findall('.//edge[@xmi:type="uml:ObjectFlow"]', namespaces)
        for object_flow in object_flows:
            m_object_flows.add(self.parse_flow_relation(object_flow, namespaces, "ObjectFlow"))
        return m_object_flows

    def parse_partitions(self, model, namespaces):
        m_partitions = set()
        partitions = set(model.findall('.//ownedMember[@xmi:type="uml:ActivityPartition"]', namespaces))
        partitions.update(model.findall('.//group[@xmi:type="uml:ActivityPartition"]', namespaces))
        for partition in partitions:
            m_partitions.add(self.parse_activity_node(partition, namespaces, "Partition"))
        return m_partitions

    def parse_partition_relations(self, model, namespaces):
        m_partition_relations = set()
        partitions = set(model.findall('.//ownedMember[@xmi:type="uml:ActivityPartition"]', namespaces))
        partitions.update(model.findall('.//group[@xmi:type="uml:ActivityPartition"]', namespaces))
        for partition in partitions:
            contained_nodes = set(set(partition.getchildren()) & set(partition.findall('.//containedNode')))
            for contained_node in contained_nodes:
                m_partition_relations.add(self.parse_partition_relation(partition, contained_node, namespaces))
        return m_partition_relations

    @staticmethod
    def parse_partition_relation(partition, contained_node, namespaces):
        try:
            rel_id = str(uuid.uuid4())
            rel_source = contained_node.attrib["{" + namespaces['xmi'] + "}" + "idref"]
            rel_target = partition.attrib["{" + namespaces['xmi'] + "}" + "id"]
            rel_type = "PartitionMember"
            return ActivityRelation(rel_id, rel_source, rel_target, rel_type)
        except Exception as exc:
            raise AttributeError("Corrupted partition or one of its member in source file") from exc

    def parse_central_buffers(self, model, namespaces):
        m_central_buffers = set()
        central_buffers = set(model.findall('.//ownedMember[@xmi:type="uml:CentralBufferNode"]', namespaces))
        central_buffers.update(model.findall('.//node[@xmi:type="uml:CentralBufferNode"]', namespaces))
        for central_buffer in central_buffers:
            m_central_buffers.add(self.parse_activity_node(central_buffer, namespaces, "CentralBuffer"))
        return m_central_buffers

    def parse_pins(self, model, namespaces):
        m_pins = set()
        m_pins.update(self.parse_input_pins(model, namespaces))
        m_pins.update(self.parse_output_pins(model, namespaces))
        return m_pins

    def parse_input_pins(self, model, namespaces):
        m_input_pins = set()
        input_pins = set(model.findall('.//argument[@xmi:type="uml:InputPin"]', namespaces))
        input_pins.update(model.findall('.//input[@xmi:type="uml:InputPin"]', namespaces))
        for input_pin in input_pins:
            m_input_pins.add(self.parse_activity_node(input_pin, namespaces, "InputPin"))
        return m_input_pins

    def parse_output_pins(self, model, namespaces):
        m_output_pins = set()
        output_pins = set(model.findall('.//result[@xmi:type="uml:OutputPin"]', namespaces))
        output_pins.update(model.findall('.//output[@xmi:type="uml:OutputPin"]', namespaces))
        for output_pin in output_pins:
            m_output_pins.add(self.parse_activity_node(output_pin, namespaces, "OutputPin"))
        return m_output_pins

    def parse_data_stores(self, model, namespaces):
        m_data_stores = set()
        data_stores = set(model.findall('.//ownedMember[@xmi:type="uml:DataStoreNode"]', namespaces))
        data_stores.update(set(model.findall('.//node[@xmi:type="uml:DataStoreNode"]', namespaces)))
        for data_store in data_stores:
            m_data_stores.add(self.parse_activity_node(data_store, namespaces, "DataStore"))
        return m_data_stores

    @staticmethod
    def parse_pin_relations(model, namespaces):
        try:
            pin_relations = set()
            actions = set(model.findall('.//ownedMember[@xmi:type="uml:CallBehaviorAction"]', namespaces))
            actions.update(model.findall('.//node[@xmi:type="uml:CallBehaviorAction"]', namespaces))
            for action in actions:
                pins = set(action.findall('.//argument[@xmi:type="uml:InputPin"]', namespaces))
                pins.update(action.findall('.//result[@xmi:type="uml:OutputPin"]', namespaces))
                pins.update(model.findall('.//output[@xmi:type="uml:OutputPin"]', namespaces))
                pins.update(model.findall('.//input[@xmi:type="uml:InputPin"]', namespaces))
                for pin in pins:
                    rel_id = str(uuid.uuid4())
                    rel_target = pin.attrib["{" + namespaces['xmi'] + "}" + "id"]
                    rel_source = action.attrib["{" + namespaces['xmi'] + "}" + "id"]
                    rel_type = "HasPin"
                    m_rel = ActivityRelation(rel_id, rel_source, rel_target, rel_type)
                    pin_relations.add(m_rel)
            return pin_relations
        except Exception as exc:
            raise AttributeError("Corrupted action or pin node in source file") from exc
