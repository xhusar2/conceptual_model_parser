import unittest
from parsers.VisualParadigmParsers.VPActivityParser import VPActivityParser
from models.activityDiagram.ActivityDiagramModel import ActivityDiagramModel
from models.activityDiagram.ActivityRelation import ActivityRelation
from models.activityDiagram.ActivityNode import ActivityNode


class TestEAActivityDiagramParser(unittest.TestCase):
    def setUp(self):
        self.test_file = "/Users/fanda/fanda/Skola_2020-2021_ZS/Bakalarka/source/conceptual_model_parser/xmiExamples/VP_Activity/OrderPayment.xmi"
        self.parser = VPActivityParser()
        self.namespaces = self.parser.get_namespaces(self.test_file)
        self.model = self.parser.get_model(self.test_file, self.namespaces)

    def test_get_namespaces(self):
        namespaces = self.parser.get_namespaces(self.test_file)
        self.assertGreaterEqual(len(namespaces), 2)
        self.assertTrue("xmi" in namespaces)
        self.assertTrue("uml" in namespaces)

    def test_get_model(self):
        model = self.parser.get_model(self.test_file, self.namespaces)
        self.assertIsNotNone(model)
        self.assertEqual(model.attrib["name"], "untitled")
        self.assertTrue('{' + self.namespaces['xmi'] + '}' + 'id' in model.attrib)

    def test_parse_model_type(self):
        model = self.parser.parse_model(self.model, self.namespaces)
        self.assertEqual(type(model), ActivityDiagramModel)

    def test_parse_nodes_no_model(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_nodes(None, self.namespaces)

    def test_parse_nodes_count(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        self.assertEqual(len(nodes), 17)

    def test_parse_nodes_type(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        for node in nodes:
            self.assertEqual(type(node), ActivityNode)

    def test_parse_relations_count(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        self.assertEqual(len(relations), 29)

    def test_parse_relations_type(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        for relation in relations:
            self.assertEqual(type(relation), ActivityRelation)

    def test_parse_relations_no_model(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_relations(None, self.namespaces)

    def test_parse_activity_node_id(self):
        input_pin = self.model.find('.//argument[@xmi:type="uml:InputPin"]', self.namespaces)
        node = self.parser.parse_activity_node(input_pin, self.namespaces, "InputPin")
        self.assertEqual(node.id, "C.Jn0x6GAqAUOAe4")

    def test_parse_activity_node_name_empty(self):
        input_pin = self.model.find('.//argument[@xmi:type="uml:InputPin"]', self.namespaces)
        node = self.parser.parse_activity_node(input_pin, self.namespaces, "InputPin")
        self.assertEqual(node.name, None)

    def test_parse_activity_node_name_exists(self):
        actions = set(self.model.findall('.//ownedMember[@xmi:type="uml:CallBehaviorAction"]', self.namespaces))
        actions.update(self.model.findall('.//node[@xmi:type="uml:CallBehaviorAction"]', self.namespaces))
        node = self.parser.parse_activity_node(list(actions)[0], self.namespaces, "Action")
        self.assertNotEqual(node.name, None)

    def test_parse_activity_node_name_data(self):
        data_stores = set(self.model.findall('.//ownedMember[@xmi:type="uml:DataStoreNode"]', self.namespaces))
        data_stores.update(set(self.model.findall('.//node[@xmi:type="uml:DataStoreNode"]', self.namespaces)))
        node = self.parser.parse_activity_node(list(data_stores)[0], self.namespaces, "DataStore")
        self.assertEqual(node.name, "Invoice data store")

    def test_parse_activity_node_type(self):
        input_pin = self.model.find('.//argument[@xmi:type="uml:InputPin"]', self.namespaces)
        node_type = "InputPin"
        node = self.parser.parse_activity_node(input_pin, self.namespaces, node_type)
        self.assertEqual(node.node_type, node_type)

    def test_parse_activity_node_visibility(self):
        input_pin = self.model.find('.//argument[@xmi:type="uml:InputPin"]', self.namespaces)
        node = self.parser.parse_activity_node(input_pin, self.namespaces, "InputPin")
        self.assertEqual(node.visibility, None)

    def test_parse_activity_node_ordering_data(self):
        input_pin = self.model.find('.//argument[@xmi:type="uml:InputPin"]', self.namespaces)
        node = self.parser.parse_activity_node(input_pin, self.namespaces, "InputPin")
        self.assertEqual(node.ordering, "FIFO")

    def test_parse_activity_node_ordering_missing(self):
        actions = set(self.model.findall('.//ownedMember[@xmi:type="uml:CallBehaviorAction"]', self.namespaces))
        actions.update(self.model.findall('.//node[@xmi:type="uml:CallBehaviorAction"]', self.namespaces))
        node = self.parser.parse_activity_node(list(actions)[0], self.namespaces, "Action")
        self.assertEqual(node.ordering, None)

    def test_parse_actions_count(self):
        actions = self.parser.parse_actions(self.model, self.namespaces)
        self.assertEqual(len(actions), 6)

    def test_parse_actions_type(self):
        actions = self.parser.parse_actions(self.model, self.namespaces)
        for action in actions:
            self.assertEqual(action.node_type, "Action")

    def test_parse_initial_nodes_count(self):
        initials = self.parser.parse_initial_nodes(self.model, self.namespaces)
        self.assertEqual(len(initials), 1)

    def test_parse_initial_nodes_type(self):
        initials = self.parser.parse_initial_nodes(self.model, self.namespaces)
        for init in initials:
            self.assertEqual(init.node_type, "Initial")

    def test_parse_activity_finals_count(self):
        finals = self.parser.parse_activity_finals(self.model, self.namespaces)
        self.assertEqual(len(finals), 1)

    def test_parse_activity_finals_type(self):
        finals = self.parser.parse_activity_finals(self.model, self.namespaces)
        for final in finals:
            self.assertEqual(final.node_type, "ActivityFinal")

    def test_parse_flow_finals_count_zero(self):
        flow_finals = self.parser.parse_flow_finals(self.model, self.namespaces)
        self.assertEqual(len(flow_finals), 0)

    def test_parse_flow_finals_count(self):
        model = self.parser.get_model(
            "/Users/fanda/fanda/Skola_2020-2021_ZS/Bakalarka/source/conceptual_model_parser/xmiExamples/VP_Activity/testingFlowBuffer.xmi",
            self.namespaces)
        flow_finals = self.parser.parse_flow_finals(model, self.namespaces)
        self.assertEqual(len(flow_finals), 1)

    def test_parse_flow_finals_type(self):
        model = self.parser.get_model(
            "/Users/fanda/fanda/Skola_2020-2021_ZS/Bakalarka/source/conceptual_model_parser/xmiExamples/VP_Activity/testingFlowBuffer.xmi",
            self.namespaces)
        flow_finals = self.parser.parse_flow_finals(model, self.namespaces)
        for flow in flow_finals:
            self.assertEqual(flow.node_type, "FlowFinal")

    def test_parse_forks_joins_count(self):
        forks_joins = self.parser.parse_forks_joins(self.model, self.namespaces)
        self.assertEqual(len(forks_joins), 2)

    def test_parse_forks_joins_type(self):
        forks_joins = self.parser.parse_forks_joins(self.model, self.namespaces)
        for node in forks_joins:
            self.assertEqual(node.node_type, "ForkJoin")

    def test_parse_decisions_merges_count(self):
        decisions_merges = self.parser.parse_decisions_merges(self.model, self.namespaces)
        self.assertEqual(len(decisions_merges), 2)

    def test_parse_decisions_merges_type(self):
        decisions_merges = self.parser.parse_decisions_merges(self.model, self.namespaces)
        for node in decisions_merges:
            self.assertEqual(node.node_type, "DecisionMerge")

    def test_parse_central_buffers_count_zero(self):
        buffers = self.parser.parse_central_buffers(self.model, self.namespaces)
        self.assertEqual(len(buffers), 0)

    def test_parse_central_buffers_count(self):
        model = self.parser.get_model(
            "/Users/fanda/fanda/Skola_2020-2021_ZS/Bakalarka/source/conceptual_model_parser/xmiExamples/VP_Activity/testingFlowBuffer.xmi",
            self.namespaces)
        buffers = self.parser.parse_central_buffers(model, self.namespaces)
        self.assertEqual(len(buffers), 1)

    def test_parse_central_buffers_type(self):
        model = self.parser.get_model(
            "/Users/fanda/fanda/Skola_2020-2021_ZS/Bakalarka/source/conceptual_model_parser/xmiExamples/VP_Activity/testingFlowBuffer.xmi",
            self.namespaces)
        buffers = self.parser.parse_central_buffers(model, self.namespaces)
        for buffer in buffers:
            self.assertEqual(buffer.node_type, "CentralBuffer")

    def test_parse_flow_relation_id(self):
        c_flow = self.model.find('.//edge[@xmi:type="uml:ControlFlow"]', self.namespaces)
        flow = self.parser.parse_flow_relation(c_flow, self.namespaces, "ControlFlow")
        self.assertEqual(flow.id, "1W2H0x6GAqAUOAac")

    def test_parse_flow_relation_type(self):
        c_flow = self.model.find('.//edge[@xmi:type="uml:ControlFlow"]', self.namespaces)
        c_type = "ControlFlow"
        flow = self.parser.parse_flow_relation(c_flow, self.namespaces, c_type)
        self.assertEqual(flow.relation_type, c_type)

    def test_parse_flow_relation_target(self):
        c_flow = self.model.find('.//edge[@xmi:type="uml:ControlFlow"]', self.namespaces)
        flow = self.parser.parse_flow_relation(c_flow, self.namespaces, "ControlFlow")
        self.assertEqual(flow.target, "8nGH0x6GAqAUOAaX")

    def test_parse_flow_relation_source(self):
        c_flow = self.model.find('.//edge[@xmi:type="uml:ControlFlow"]', self.namespaces)
        flow = self.parser.parse_flow_relation(c_flow, self.namespaces, "ControlFlow")
        self.assertEqual(flow.source, "bIaH0x6GAqAUOAaK")

    def test_parse_flow_relation_guard_empty(self):
        c_flow = self.model.find('.//edge[@xmi:type="uml:ControlFlow"]', self.namespaces)
        flow = self.parser.parse_flow_relation(c_flow, self.namespaces, "ControlFlow")
        self.assertEqual(flow.guard, None)

    def test_parse_flow_relation_guard_exists(self):
        c_flow = self.model.find('.//edge[@xmi:type="uml:ControlFlow"][@xmi:id="jbAn0x6GAqAUOAcn"]', self.namespaces)
        flow = self.parser.parse_flow_relation(c_flow, self.namespaces, "ControlFlow")
        self.assertEqual(flow.guard, "Yes")

    def test_parse_flow_relation_error(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_flow_relation(None, self.namespaces, "ControlFlow")

    def test_parse_control_flows_count(self):
        controls = self.parser.parse_control_flows(self.model, self.namespaces)
        self.assertEqual(len(controls), 12)

    def test_parse_control_flows_type(self):
        controls = self.parser.parse_control_flows(self.model, self.namespaces)
        for control in controls:
            self.assertEqual(control.relation_type, "ControlFlow")

    def test_parse_object_flows_count(self):
        objects = self.parser.parse_object_flows(self.model, self.namespaces)
        self.assertEqual(len(objects), 2)

    def test_parse_object_flows_type(self):
        objects = self.parser.parse_object_flows(self.model, self.namespaces)
        for o in objects:
            self.assertEqual(o.relation_type, "ObjectFlow")

    def test_parse_partitions_count(self):
        partitions = self.parser.parse_partitions(self.model, self.namespaces)
        self.assertEqual(len(partitions), 2)

    def test_parse_partitions_type(self):
        partitions = self.parser.parse_partitions(self.model, self.namespaces)
        for partition in partitions:
            self.assertEqual(partition.node_type, "Partition")

    def test_parse_partition_relations_count(self):
        rels = self.parser.parse_partition_relations(self.model, self.namespaces)
        self.assertEqual(len(rels), 13)

    def test_parse_partition_relations_type(self):
        rels = self.parser.parse_partition_relations(self.model, self.namespaces)
        for rel in rels:
            self.assertEqual(rel.relation_type, "PartitionMember")

    def test_parse_flow_relation_error(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_flow_relation(None, self.namespaces, "ControlFlow")

    def test_parse_partition_relation(self):
        pass

    def test_parse_pins_count(self):
        pins = self.parser.parse_pins(self.model, self.namespaces)
        self.assertEqual(len(pins), 2)

    def test_parse_pins_type(self):
        pins = self.parser.parse_pins(self.model, self.namespaces)
        for pin in pins:
            self.assertTrue("Pin" in pin.node_type)

    def test_parse_input_pins_count(self):
        input_pins = self.parser.parse_input_pins(self.model, self.namespaces)
        self.assertEqual(len(input_pins), 1)

    def test_parse_input_pins_type(self):
        input_pins = self.parser.parse_input_pins(self.model, self.namespaces)
        for pin in input_pins:
            self.assertEqual(pin.node_type, "InputPin")

    def test_parse_output_pins_count(self):
        output_pins = self.parser.parse_output_pins(self.model, self.namespaces)
        self.assertEqual(len(output_pins), 1)

    def test_parse_output_pins_type(self):
        output_pins = self.parser.parse_output_pins(self.model, self.namespaces)
        for pin in output_pins:
            self.assertEqual(pin.node_type, "OutputPin")

    def test_parse_data_stores_count(self):
        stores = self.parser.parse_data_stores(self.model, self.namespaces)
        self.assertEqual(len(stores), 1)

    def test_parse_data_stores_type(self):
        stores = self.parser.parse_data_stores(self.model, self.namespaces)
        for store in stores:
            self.assertEqual(store.node_type, "DataStore")

    def test_parse_pin_relations_count(self):
        rels = self.parser.parse_pin_relations(self.model, self.namespaces)
        self.assertEqual(len(rels), 2)

    def test_parse_pin_relations_type(self):
        rels = self.parser.parse_pin_relations(self.model, self.namespaces)
        for rel in rels:
            self.assertEqual(rel.relation_type, "HasPin")

    def test_parse_relations_unique_id(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        ids = set()
        for relation in relations:
            ids.add(relation.id)
        self.assertEqual(len(ids), len(relations))

    def test_parse_nodes_unique_id(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        ids = set()
        for node in nodes:
            ids.add(node.id)
        self.assertEqual(len(ids), len(nodes))

    def test_unique_ids(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        ids = set()
        for relation in relations:
            ids.add(relation.id)
        for node in nodes:
            ids.add(node.id)
        self.assertEqual(len(ids), len(relations) + len(nodes))
