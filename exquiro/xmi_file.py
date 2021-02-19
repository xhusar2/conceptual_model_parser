from lxml import etree


class XMIFile:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_diagrams(self):
        return ['class_diagram']

    def get_namespaces(self, file_name):
        return etree.parse(file_name).getroot().nsmap

    # identifies format file
    def get_format(self):
        root = etree.parse(self.file_path).getroot()
        namespaces = self.get_namespaces(self.file_path)
        # try find exporter (EA format)
        exporter = root.find('xmi:Documentation', namespaces)
        if exporter is not None and 'exporter' in exporter.attrib:
            # print('format: ',exporter.attrib['exporter'])
            return "enterprise_architect"
        # openPonk format
        applied_profile = root.find('.//appliedProfile', namespaces)
        if applied_profile is not None and 'href' in applied_profile.attrib:
            # print('format: openPonk')
            return 'open_ponk'
        return ''
