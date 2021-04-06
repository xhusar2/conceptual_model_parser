import unittest
from parsers.VisualParadigmParsers.VPPackageParser import VPPackageParser
from models.packageDiagram.PackageNode import PackageNode
from models.packageDiagram.PackageRelation import PackageRelation
from models.packageDiagram.PackageDiagramModel import PackageDiagramModel


class TestEAPackageDiagramParser(unittest.TestCase):
    def setUp(self):
        self.test_file = "/Users/fanda/fanda/Skola_2020-2021_ZS/Bakalarka/source/conceptual_model_parser/xmiExamples/VP_Package/ShoppingSystem.xmi"
        self.parser = VPPackageParser()
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
        self.assertEqual(model.attrib["{" + self.namespaces['xmi'] + "}" + "id"], "P2gshR6GAqAUIAYR")
        self.assertFalse('{' + self.namespaces['xmi'] + '}' + 'type' in model.attrib)

    def test_parse_packages_count(self):
        packages = self.parser.parse_packages(self.model, self.namespaces)
        self.assertEqual(len(packages), 10)

    def test_parse_packages_type(self):
        packages = self.parser.parse_packages(self.model, self.namespaces)
        for package in packages:
            self.assertEqual(type(package), PackageNode)
            self.assertEqual(package.node_type, "Package")

    def test_parse_package_type(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        package = self.parser.parse_package(packages[0], self.namespaces)
        self.assertEqual(package.node_type, "Package")

    def test_parse_package_id(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        package = self.parser.parse_package(packages[0], self.namespaces)
        self.assertEqual(package.id, "e9WshR6GAqAUIAmX")

    def test_parse_package_name(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        package = self.parser.parse_package(packages[0], self.namespaces)
        self.assertEqual(package.name, "ShoppingType")

    def test_parse_package_visibility(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
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

    def test_parse_supplier_client_relation_type(self):
        dependencies = self.model.findall('.//ownedMember[@xmi:type="uml:Dependency"]', self.namespaces)
        dependency = self.parser.parse_supplier_client_relation(dependencies[0], self.namespaces, "Dependency")
        self.assertEqual(dependency.relation_type, "Dependency")

    def test_parse_supplier_client_relation_id(self):
        dependencies = self.model.findall('.//ownedMember[@xmi:type="uml:Dependency"]', self.namespaces)
        dependency = self.parser.parse_supplier_client_relation(dependencies[0], self.namespaces, "Dependency")
        self.assertEqual(dependency.id, "Iv_chR6GAqAUIApg")

    def test_parse_supplier_client_relation_source(self):
        dependencies = self.model.findall('.//ownedMember[@xmi:type="uml:Dependency"]', self.namespaces)
        dependency = self.parser.parse_supplier_client_relation(dependencies[0], self.namespaces, "Dependency")
        self.assertEqual(dependency.source, "e9WshR6GAqAUIAmX")

    def test_parse_supplier_client_relation_target(self):
        dependencies = self.model.findall('.//ownedMember[@xmi:type="uml:Dependency"]', self.namespaces)
        dependency = self.parser.parse_supplier_client_relation(dependencies[0], self.namespaces, "Dependency")
        self.assertEqual(dependency.target, "T.9shR6GAqAUIAnB")

    def test_parse_supplier_client_relation_empty(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_supplier_client_relation(None, self.namespaces, "None")

    def test_parse_supplier_client_relation_error(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_supplier_client_relation("error", self.namespaces, "None")

    def test_parse_merges_count(self):
        merges = self.parser.parse_merges(self.model, self.namespaces)
        self.assertEqual(len(merges), 1)

    def test_parse_merges_type(self):
        merges = self.parser.parse_merges(self.model, self.namespaces)
        for merge in merges:
            self.assertEqual(merge.relation_type, "PackageMerge")

    def test_parse_imports_count(self):
        imports = self.parser.parse_imports(self.model, self.namespaces)
        self.assertEqual(len(imports), 3)

    def test_parse_public_imports_count(self):
        imports = self.parser.parse_imports(self.model, self.namespaces)
        public_imports = set()
        for import_e in imports:
            if import_e.relation_type == "PackageImport":
                public_imports.add(import_e)
        self.assertEqual(len(public_imports), 2)

    def test_parse_private_imports_count(self):
        imports = self.parser.parse_imports(self.model, self.namespaces)
        public_imports = set()
        for import_e in imports:
            if import_e.relation_type == "PackageAccess":
                public_imports.add(import_e)
        self.assertEqual(len(public_imports), 1)

    def test_parse_imports_type(self):
        imports = self.parser.parse_imports(self.model, self.namespaces)
        for m_import in imports:
            self.assertEqual(type(m_import), PackageRelation)

    def test_parse_public_import_type(self):
        import_e = self.model.findall('.//packageImport', self.namespaces)[0]
        parsed_import = self.parser.parse_import(import_e, self.namespaces)
        self.assertEqual(parsed_import.relation_type, "PackageImport")

    def test_parse_private_import_type(self):
        import_e = self.model.findall('.//packageImport', self.namespaces)[1]
        parsed_import = self.parser.parse_import(import_e, self.namespaces)
        self.assertEqual(parsed_import.relation_type, "PackageAccess")

    def test_parse_import_id(self):
        import_e = self.model.findall('.//packageImport', self.namespaces)[0]
        parsed_import = self.parser.parse_import(import_e, self.namespaces)
        self.assertEqual(parsed_import.id, "7C2chR6GAqAUIAoD")

    def test_parse_import_source(self):
        import_e = self.model.findall('.//packageImport', self.namespaces)[0]
        parsed_import = self.parser.parse_import(import_e, self.namespaces)
        self.assertEqual(parsed_import.source, "T.9shR6GAqAUIAnB")

    def test_parse_import_target(self):
        import_e = self.model.findall('.//packageImport', self.namespaces)[0]
        parsed_import = self.parser.parse_import(import_e, self.namespaces)
        self.assertEqual(parsed_import.target, "44zshR6GAqAUIAnT")

    def test_parse_import_empty(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_import(None, self.namespaces)

    def test_parse_import_error(self):
        with self.assertRaises(AttributeError):
            self.parser.parse_import("error", self.namespaces)

    def test_parse_member_packages_count(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        members = self.parser.parse_member_packages(packages, self.namespaces)
        self.assertEqual(len(members), 9)

    def test_parse_member_packages_type(self):
        packages = self.parser.get_packages(self.model, self.namespaces)
        members = self.parser.parse_member_packages(packages, self.namespaces)
        for member in members:
            self.assertEqual(type(member), PackageRelation)

    def test_parse_member_package_type(self):
        package = self.parser.get_packages(self.model, self.namespaces)[0]
        member = package.getchildren()[1]
        parsed_member = self.parser.parse_member_package(member, package, self.namespaces)
        self.assertEqual(parsed_member.relation_type, "MemberOf")

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
        self.assertEqual(len(ids), len(nodes))

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
        self.assertEqual(len(ids), len(relations))

    def test_parse_relations_type(self):
        relations = self.parser.parse_relations(self.model, self.namespaces)
        for relation in relations:
            self.assertEqual(type(relation), PackageRelation)

    def test_is_package_package(self):
        package = self.parser.get_packages(self.model, self.namespaces)[0]
        self.assertTrue(self.parser.is_package(package, self.namespaces))

    def test_is_package_relation(self):
        relation = self.model.findall('.//ownedMember[@xmi:type="uml:Dependency"]', self.namespaces)[0]
        self.assertFalse(self.parser.is_package(relation, self.namespaces))
