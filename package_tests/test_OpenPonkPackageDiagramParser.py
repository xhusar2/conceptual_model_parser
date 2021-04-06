import unittest
from parsers.OpenponkParsers.OpenPonkPackageDiagramParser import OpenPonkPackageDiagramParser
from models.packageDiagram.PackageNode import PackageNode
from models.packageDiagram.PackageRelation import PackageRelation
from models.packageDiagram.PackageDiagramModel import PackageDiagramModel


class TestEAPackageDiagramParser(unittest.TestCase):
    def setUp(self):
        self.test_file = "/Users/fanda/fanda/Skola_2020-2021_ZS/Bakalarka/source/conceptual_model_parser/xmiExamples/OP_Package/ShoppingSystem.xmi"
        self.parser = OpenPonkPackageDiagramParser()
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
        self.assertEqual(model.attrib["name"], "Shopping System")
        self.assertEqual(model.attrib["{" + self.namespaces['xmi'] + "}" + "type"], "uml:Package")
        self.assertEqual(model.attrib["{" + self.namespaces['xmi'] + "}" + "id"], "9d1bf8df-987b-0d00-adb9-d43d0fcf975a")

    def test_parse_packages_count(self):
        packages = self.parser.parse_packages(self.model, self.namespaces)
        self.assertEqual(len(packages), 6)

    def test_parse_packages_type(self):
        packages = self.parser.parse_packages(self.model, self.namespaces)
        for package in packages:
            self.assertEqual(type(package), PackageNode)
            self.assertEqual(package.node_type, "Package")

    def test_parse_package_type(self):
        packages = self.model.findall('.//packagedElement[@xmi:type="uml:Package"]', self.namespaces)
        package = self.parser.parse_package(packages[0], self.namespaces)
        self.assertEqual(package.node_type, "Package")

    def test_parse_package_id(self):
        packages = self.model.findall('.//packagedElement[@xmi:type="uml:Package"]', self.namespaces)
        package = self.parser.parse_package(packages[0], self.namespaces)
        self.assertEqual(package.id, "721ef8df-987b-0d00-adba-fef20fcf975a")

    def test_parse_package_name(self):
        packages = self.model.findall('.//packagedElement[@xmi:type="uml:Package"]', self.namespaces)
        package = self.parser.parse_package(packages[0], self.namespaces)
        self.assertEqual(package.name, "Shopping Cart")

    def test_parse_package_visibility(self):
        packages = self.model.findall('.//packagedElement[@xmi:type="uml:Package"]', self.namespaces)
        package = self.parser.parse_package(packages[0], self.namespaces)
        self.assertEqual(package.visibility, "public")

    def test_parse_package_empty(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_package(None, self.namespaces)

    def test_parse_package_error(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_package("error", self.namespaces)

    def test_parse_imports_count(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        imports = self.parser.parse_imports(packages, self.namespaces)
        self.assertEqual(len(imports), 3)

    def test_parse_imports_type(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        imports = self.parser.parse_imports(packages, self.namespaces)
        for m_import in imports:
            self.assertEqual(type(m_import), PackageRelation)

    def test_parse_import_type(self):
        pass

    def test_parse_import_id(self):
        pass

    def test_parse_import_source(self):
        pass

    def test_parse_import_target(self):
        pass

    def test_parse_import_empty(self):
        package = self.parser.get_packages(self.model, self.namespaces)[0]
        with self.assertRaises(AttributeError):
            self.parser.parse_import(None, package, self.namespaces)

    def test_parse_import_error(self):
        package = self.parser.get_packages(self.model, self.namespaces)[0]
        with self.assertRaises(AttributeError):
            self.parser.parse_import("error", package, self.namespaces)

    def test_parse_member_packages_count(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        members = self.parser.parse_member_packages(packages, self.namespaces)
        self.assertEqual(len(members), 5)

    def test_parse_member_packages_type(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        members = self.parser.parse_member_packages(packages, self.namespaces)
        for member in members:
            self.assertEqual(type(member), PackageRelation)

    def test_parse_member_package_type(self):
        package = self.parser.get_packages(self.model, self.namespaces)[5]
        members = list(set(package.findall('.//packagedElement[@xmi:type="uml:Package"]', self.namespaces)) &
                       set(package.getchildren()))
        parsed_member = self.parser.parse_member_package(members[0], package, self.namespaces)
        self.assertEqual(parsed_member.relation_type, "MemberOf")

    def test_get_packages_count(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        self.assertEqual(len(packages), 6)

    def test_parse_model(self):
        parsed_model = self.parser.parse_model(self.model, self.namespaces)
        self.assertEqual(type(parsed_model), PackageDiagramModel)

    def test_parse_file(self):
        parsed_model = self.parser.parse_file(self.test_file)
        self.assertEqual(type(parsed_model), PackageDiagramModel)

    def test_parse_nodes_count(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        self.assertEqual(len(nodes), 6)

    def test_parse_nodes_unique_id(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        ids = set()
        for node in nodes:
            ids.add(node.id)
        self.assertEqual(len(ids), len(nodes))

    def test_parse_nodes_type(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        for node in nodes:
            self.assertEqual(type(node), PackageNode)

    def test_parse_relations_count(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        self.assertEqual(len(relations), 8)

    def test_parse_relations_unique_id(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        ids = set()
        for relation in relations:
            ids.add(relation.id)
        self.assertEqual(len(ids), len(relations))

    def test_parse_relations_type(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        for relation in relations:
            self.assertEqual(type(relation), PackageRelation)
