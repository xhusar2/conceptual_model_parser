import unittest
from model.Model import Model


class TestModelParsing(unittest.TestCase):
    input_file = "../xmi_examples/EA_Class_basic.xml"

    def test_parse_simple_model(self):
        with open(self.input_file, 'r') as f:
            model_string = f.read()
            m = Model("testModel", model_string)
            m.parse_model()
            self.assertEqual(len(m.relations),1)


if __name__ == '__main__':
    unittest.main()