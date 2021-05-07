from lxml import etree


class XMIFile:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_diagrams(self):
        # TODO - implement hierarchical system of picking diagrams in a iterative manner and choosing the best possible
        return ['class_diagram']

    def get_namespaces(self, file_name):
        return etree.parse(file_name).getroot().nsmap

    # identifies format file, assume format is openponk as no format marks are provide
    def get_format(self):
        root = etree.parse(self.file_path).getroot()
        namespaces = self.get_namespaces(self.file_path)
        # try find exporter (EA format)
        exporter = root.find('xmi:Documentation', namespaces)
        if exporter is not None and 'exporter' in exporter.attrib and exporter.attrib["exporter"] == "Visual Paradigm":
            return "visual_paradigm"
        if exporter is not None and 'exporter' in exporter.attrib and exporter.attrib["exporter"] == "Enterprise Architect":
            return "enterprise_architect"
        # openPonk format
        applied_profile = root.find('.//appliedProfile', namespaces)
        if applied_profile is not None and 'href' in applied_profile.attrib:
            return 'open_ponk'
        return 'open_ponk'
