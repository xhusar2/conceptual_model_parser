import unittest
from ..parsers.enterprise_architect.ea_class_diagram_parser import EaClsDiagramParser
from ..models.class_diagram.class_diagram_model import ClsDiagramModel
from ..models.class_diagram.class_node import ClassNode


class TestEAClassDiagramParser(unittest.TestCase):
    def setUp(self):
        self.test_file = "exquiro/tests/test_models/ea_class_basic.xml"
        self.test_file_advanced = "exquiro/tests/test_models/ea_case_advanced.xmi"
        self.parser = EaClsDiagramParser()
        self.namespaces = self.parser.get_namespaces(self.test_file)
        self.model = self.parser.get_model(self.test_file, self.namespaces)
        self.model_advanced = self.parser.get_model(self.test_file_advanced, self.namespaces)

    def test_get_namespaces(self):
        namespaces = self.parser.get_namespaces(self.test_file)
        self.assertGreaterEqual(len(namespaces), 2)
        self.assertTrue("xmi" in namespaces)
        self.assertTrue("uml" in namespaces)

    def test_get_model(self):
        model = self.parser.get_model(self.test_file, self.namespaces)
        self.assertIsNotNone(model)
        self.assertEqual(model.attrib["name"], "EA_Model")
        self.assertEqual(model.attrib["{" + self.namespaces['xmi'] + "}" + "type"], "uml:Model")
        self.assertFalse('{' + self.namespaces['xmi'] + '}' + 'id' in model.attrib)

    def test_parse_model(self):
        parsed_model = self.parser.parse_model(self.model, self.namespaces)
        self.assertEqual(type(parsed_model), ClsDiagramModel)

    def test_parse_file(self):
        parsed_model = self.parser.parse_file(self.test_file)
        self.assertEqual(type(parsed_model), ClsDiagramModel)

    def test_parse_classes_type(self):
        classes = self.parser.parse_classes(self.model, self.namespaces)
        for cls in classes:
            self.assertEqual(type(cls), ClassNode)

    def test_parse_associations_count(self):
        associations = self.parser.parse_associations(self.model, self.namespaces)
        self.assertEqual(len(associations), 2)

    def test_parse_enumerations_count(self):
        enumerations = self.parser.parse_enumerations(self.model, self.namespaces)
        self.assertEqual(len(enumerations), 0)

    def test_parse_enumerations_adv_count(self):
        enumerations = self.parser.parse_enumerations(self.model_advanced, self.namespaces)
        self.assertEqual(len(enumerations), 2)

    def test_parse_attributes_adv_count(self):
        attributes = self.parser.parse_attributes(self.model_advanced, self.namespaces)
        self.assertEqual(len(attributes), 0)

    def test_parse_generalizations_adv_count(self):
        generalizations = self.parser.parse_generalizations(self.model_advanced, self.namespaces)
        self.assertEqual(len(generalizations), 0)

    def test_parse_generalization_sets_adv_count(self):
        gs = self.parser.parse_generalization_sets(self.model_advanced, self.namespaces)
        self.assertEqual(len(gs), 0)