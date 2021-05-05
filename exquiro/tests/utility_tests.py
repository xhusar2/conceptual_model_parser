import unittest
from ..models.class_diagram.class_diagram_model import ClsDiagramModel
from ..xmi_file import XMIFile
from ..neo4j_manager import Neo4jManager


class TestNeo4jManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "exquiro/tests/openponk_class_basic.xmi"
        DATABASE_URL = f'bolt://neo4j:password@localhost:7687'
        self.neo4j_manager = Neo4jManager(DATABASE_URL)
        self.dummy_model = ClsDiagramModel("test_id", [], [], [], [], [], [], [], [], [], [], [], [])

    def test_delete_all(self):
        self.assertTrue(self.neo4j_manager.delete_all())

    def test_delete_model(self):
        self.assertTrue(self.neo4j_manager.delete_model("dummy"))

    def test_add_model(self):
        self.assertTrue(self.neo4j_manager.add_model(self.dummy_model))

class TestXMIFile(unittest.TestCase):
    def setUp(self):
        self.test_file_op = "exquiro/tests/test_models/openponk_class_basic.xmi"
        self.test_file_ea = "exquiro/tests/test_models/ea_class_basic.xml"
        self.dummy_file_op = XMIFile(self.test_file_op)
        self.dummy_file_ea = XMIFile(self.test_file_ea)

    def test_get_diagrams_ea(self):
        self.assertEqual(self.dummy_file_ea.get_diagrams(), ['class_diagram'])

    def test_get_format_ea(self):
        self.assertEqual(self.dummy_file_ea.get_format(), "enterprise_architect")

    def test_get_format_op(self):
        self.assertEqual(self.dummy_file_op.get_format(), "open_ponk")