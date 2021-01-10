import unittest
from model.Model import ClassDiagramModel


class TestModelParsing(unittest.TestCase):
    input_file = "../xmiExamples/EA_Class_basic.xml"

    def test_parse_simple_model(self):
        with open(self.input_file, 'r') as f:
            model_string = f.read()
            m = ClassDiagramModel("testModel", model_string)
            m.parse_model()
            self.assertEqual(len(m.relations),1)


if __name__ == '__main__':
    unittest.main()