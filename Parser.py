from model.ModelParsed import ModelParsed
from model.ModelEnterpriseArchitect import ModelEnterpriseArchitect
from model.ModelOpenPonk import ModelOpenPonk
from lxml import etree


def parse_enterprise_architect(file):
    # conceptual model from xmi/xml
    ea_model = ModelEnterpriseArchitect(file)
    return parse_model(ea_model)


def parse_openponk(file):
    openponk_model = ModelOpenPonk(file)
    return parse_model(openponk_model)

PARSERS = {
    'enterprise_architect': parse_enterprise_architect,
    'open_ponk' : parse_openponk
}


def get_file_format(file_name):
    root = etree.parse(file_name).getroot()
    namespaces = get_namespaces(file_name)
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


def get_namespaces(file_name):
    return etree.parse(file_name).getroot().nsmap


def parse_model(model):
    model.parse_model()
    c_types, a_types = model.get_types()
    parsed_model = ModelParsed(model.get_model_id(), model.get_classes(), model.get_associations()
                               , model.get_generalizations(), model.get_gsets(), c_types, a_types)
    return parsed_model


# Input: xmi/xml file
# Output parsed model ready to be stored to Neo4j
def parse_file( file_name):
    # get file format
    # TODO raise error when format not recognized
    print("Getting file format...")
    model_format = get_file_format(file_name)
    print("file format is:", model_format)
    # call right parser for file format
    if model_format in PARSERS:
        parse = PARSERS[model_format]
        model = parse(file_name)
        return model
    else:
        print(f'could not find format for file {file_name}!')
    return None




