import unittest
from parsers.EnterpriceArchitectParsers.EAPackageDiagramParser import EAPackageDiagramParser
from models.packageDiagram.PackageNode import PackageNode
from models.packageDiagram.PackageRelation import PackageRelation
from models.packageDiagram.PackageDiagramModel import PackageDiagramModel


class TestEAPackageDiagramParser(unittest.TestCase):
    def setUp(self):
        self.test_file = "/Users/fanda/fanda/Skola_2020-2021_ZS/Bakalarka/source/conceptual_model_parser/xmiExamples/EA_Package/ShoppingSystem.xml"
        self.parser = EAPackageDiagramParser()
        self.namespaces = self.parser.get_namespaces(self.test_file)
        self.model = self.parser.get_model(self.test_file, self.namespaces)

    def test_get_namespaces(self):
        namespaces = self.parser.get_namespaces(self.test_file)
        self.assertEqual(len(namespaces), 3)
        keys = list(namespaces.keys())
        self.assertEqual(keys[0], 'uml')
        self.assertEqual(keys[1], 'xmi')
        self.assertEqual(keys[2], 'EAUML')

    def test_get_model(self):
        model = self.parser.get_model(self.test_file, self.namespaces)
        self.assertIsNotNone(model)
        self.assertEqual(model.attrib["name"], "EA_Model")
        self.assertEqual(model.attrib["{" + self.namespaces['xmi'] + "}" + "type"], "uml:Model")
        self.assertFalse('{' + self.namespaces['xmi'] + '}' + 'id' in model.attrib)

    def test_parse_packages_count(self):
        packages = self.parser.parse_packages(self.model, self.namespaces)
        self.assertEqual(len(packages), 10)

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
        self.assertEqual(package.id, "EAPK_1748616D_AE11_4554_B148_DE4964A9B9EC")

    def test_parse_package_name(self):
        packages = self.model.findall('.//packagedElement[@xmi:type="uml:Package"]', self.namespaces)
        package = self.parser.parse_package(packages[0], self.namespaces)
        self.assertEqual(package.name, "Shopping system")

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

    def test_parse_dependencies_count(self):
        dependencies = self.parser.parse_dependencies(self.model, self.namespaces)
        self.assertEqual(len(dependencies), 1)

    def test_parse_dependencies_type(self):
        dependencies = self.parser.parse_dependencies(self.model, self.namespaces)
        for dependency in dependencies:
            self.assertEqual(dependency.relation_type, "Dependency")

    def test_parse_dependency_type(self):
        dependencies = self.model.findall('.//packagedElement[@xmi:type="uml:Dependency"]', self.namespaces)
        dependency = self.parser.parse_dependency(dependencies[0], self.namespaces)
        self.assertEqual(dependency.relation_type, "Dependency")

    def test_parse_dependency_id(self):
        dependencies = self.model.findall('.//packagedElement[@xmi:type="uml:Dependency"]', self.namespaces)
        dependency = self.parser.parse_dependency(dependencies[0], self.namespaces)
        self.assertEqual(dependency.id, "EAID_D846BF77_745B_4a92_AAEB_18B4E7C60BA0")

    def test_parse_dependency_source(self):
        dependencies = self.model.findall('.//packagedElement[@xmi:type="uml:Dependency"]', self.namespaces)
        dependency = self.parser.parse_dependency(dependencies[0], self.namespaces)
        self.assertEqual(dependency.source, "EAPK_C1A881F3_3D0B_427a_AFA3_0645530CC67C")

    def test_parse_dependency_target(self):
        dependencies = self.model.findall('.//packagedElement[@xmi:type="uml:Dependency"]', self.namespaces)
        dependency = self.parser.parse_dependency(dependencies[0], self.namespaces)
        self.assertEqual(dependency.target, "EAPK_948CB355_7F8A_4679_AC47_CA3A4D4EEBF3")

    def test_parse_dependency_empty(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_dependency(None, self.namespaces)

    def test_parse_dependency_error(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_dependency("error", self.namespaces)

    def test_parse_merges_count(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        merges = self.parser.parse_merges(packages, self.namespaces)
        self.assertEqual(len(merges), 1)

    def test_parse_merges_type(self):
        merges = self.parser.parse_merges(self.model, self.namespaces)
        for merge in merges:
            self.assertEqual(merge.relation_type, "PackageMerge")

    def test_parse_merge_type(self):
        pass

    def test_parse_merge_id(self):
        pass

    def test_parse_merge_source(self):
        pass

    def test_parse_merge_target(self):
        pass

    def test_parse_imports_count(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        imports = self.parser.parse_imports(packages, self.namespaces)
        self.assertEqual(len(imports), 2)

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

    def test_parse_member_packages(self):
        pass

    def test_parse_member_package(self):
        pass

    def test_parse_usages_count(self):
        usages = self.parser.parse_usages(self.model, self.namespaces)
        self.assertEqual(len(usages), 1)

    def test_parse_usages_type(self):
        usages = self.parser.parse_usages(self.model, self.namespaces)
        for usage in usages:
            self.assertEqual(usage.relation_type, "Usage")

    def test_parse_usage_type(self):
        usages = self.model.findall('.//packagedElement[@xmi:type="uml:Usage"]', self.namespaces)
        usage = self.parser.parse_usage(usages[0], self.namespaces)
        self.assertEqual(usage.relation_type, "Usage")

    def test_parse_usage_id(self):
        usages = self.model.findall('.//packagedElement[@xmi:type="uml:Usage"]', self.namespaces)
        usage = self.parser.parse_usage(usages[0], self.namespaces)
        self.assertEqual(usage.id, "EAID_408C4906_C7B3_46b0_8989_4B11A2E5C7F3")

    def test_parse_usage_source(self):
        usages = self.model.findall('.//packagedElement[@xmi:type="uml:Usage"]', self.namespaces)
        usage = self.parser.parse_usage(usages[0], self.namespaces)
        self.assertEqual(usage.source, "EAPK_90C0EA89_B767_4128_B044_5B4F4DB28599")

    def test_parse_usage_target(self):
        usages = self.model.findall('.//packagedElement[@xmi:type="uml:Usage"]', self.namespaces)
        usage = self.parser.parse_usage(usages[0], self.namespaces)
        self.assertEqual(usage.target, "EAPK_C1A881F3_3D0B_427a_AFA3_0645530CC67C")

    def test_get_packages_count(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        self.assertEqual(len(packages), 10)

    def test_parse_model(self):
        parsed_model = self.parser.parse_model(self.model, self.namespaces)
        self.assertEqual(type(parsed_model), PackageDiagramModel)

    def test_parse_file(self):
        parsed_model = self.parser.parse_file(self.test_file)
        self.assertEqual(type(parsed_model), PackageDiagramModel)

    def test_parse_nodes_count(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        self.assertEqual(len(nodes), 10)

    def test_parse_nodes_unique_id(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        ids = set()
        for node in nodes:
            ids.add(node.id)
        self.assertEqual(len(ids), 10)

    def test_parse_nodes_type(self):
        nodes = self.parser.parse_nodes(self.model, self.namespaces)
        for node in nodes:
            self.assertEqual(type(node), PackageNode)

    def test_parse_relations_count(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        self.assertEqual(len(relations), 14)

    def test_parse_relations_unique_id(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        ids = set()
        for relation in relations:
            ids.add(relation.id)
        self.assertEqual(len(ids), 14)

    def test_parse_relations_type(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        for relation in relations:
            self.assertEqual(type(relation), PackageRelation)

