
from models.classDiagram.ModelParsed import ModelParsed as CdModelParsed
from models.classDiagram.ModelEnterpriseArchitect import ModelEnterpriseArchitect
from models.classDiagram.ModelOpenPonk import ModelOpenPonk
from lxml import etree
from parsers.ParserInterface import ParserInterface


class ClassDiagramParser(ParserInterface):

    def parse_ea_class_diagram(self, file):
        # conceptual model from xmi/xml
        ea_model = ModelEnterpriseArchitect(file)
        return self.parse_model(ea_model)

    def parse_openponk_class_diagram(self, file):
        openponk_model = ModelOpenPonk(file)
        return self.parse_model(openponk_model)

    PARSER_DISPATCHER = {
        'enterprise_architect': parse_ea_class_diagram,
        'open_ponk':  parse_openponk_class_diagram
    }

    def parse_model(self, model):
        model.parse_model()
        c_types, a_types = model.get_types()
        parsed_model = CdModelParsed(model.get_model_id(), model.get_classes(), model.get_associations(),
                                   model.get_association_nodes()
                                   , model.get_generalizations(), model.get_gsets(), c_types, a_types)
        return parsed_model

    # Input: xmi/xml file
    # Output parsed model ready to be stored to Neo4j
    def parse_file(self, file_name, model_format):
        models = []
        # TODO raise error when format not recognized
        # call right parser for file format
        if model_format in self.PARSER_DISPATCHER:
            parse = self.PARSER_DISPATCHER[model_format]
            model = parse(self, file_name)
            models.append(model)

        else:
            print(f'could not find format for file {file_name}!')
        return models
