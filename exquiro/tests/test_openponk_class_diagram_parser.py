import unittest
from ..parsers.openponk.openpondk_class_diagram_parser import OpenponkClsDiagramParser
from ..models.class_diagram.class_diagram_model import ClsDiagramModel
from ..models.class_diagram.class_node import ClassNode


class TestOpenponkClassDiagramParser(unittest.TestCase):
    def setUp(self):
        self.test_file = "exquiro/tests/test_models/openponk_class_basic.xmi"
        self.parser = OpenponkClsDiagramParser()
        self.namespaces = self.parser.get_namespaces(self.test_file)
        self.root = self.parser.get_root(self.test_file)
        self.model = self.parser.get_model(self.test_file, self.namespaces)

    def test_get_namespaces(self):
        namespaces = self.parser.get_namespaces(self.test_file)
        self.assertGreaterEqual(len(namespaces), 2)
        self.assertTrue("xmi" in namespaces)
        self.assertTrue("uml" in namespaces)

    def test_get_model(self):
        model = self.parser.get_model(self.test_file, self.namespaces)
        self.assertIsNotNone(model)
        self.assertEqual(model.attrib["name"], "Openponk project")
        self.assertEqual(model.attrib["{" + self.namespaces['xmi'] + "}" + "type"], "uml:Model")
        self.assertTrue('{' + self.namespaces['xmi'] + '}' + 'id' in model.attrib)

    def test_parse_model(self):
        parsed_model = self.parser.parse_model(self.model, self.root, self.namespaces)
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

