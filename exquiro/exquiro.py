from .xmi_file import XMIFile
from .neo4j_manager import Neo4jManager
from .git_connector import get_xmi_files
from .parsers.parser_factory import ParserFactory
from .parsers.enterprise_architect.ea_class_diagram_parser import  EaClsDiagramParser
from .parsers.openponk.openpondk_class_diagram_parser import OpenponkClsDiagramParser
from configparser import ConfigParser
import requests
#: Paths to default configuration files
DEFAULT_CONFIG_FILES = [
    '../config/neo4j.cfg'
]

#: Author of the application
AUTHOR = 'Richard Husar'
#: Name of the application
PROG_NAME = 'exquiro'
#: Actual release tag
RELEASE = '0.4'
#: Actual version
VERSION = '0.1'


class Exquiro():
    def __init__(self, DATABASE_URL):
        self.neo4j_manager = Neo4jManager(DATABASE_URL)
        self.factory = ParserFactory()
        self.factory.register_parser('enterprise_architect', 'class_diagram', EaClsDiagramParser)
        self.factory.register_parser('open_ponk', 'class_diagram', OpenponkClsDiagramParser)

    def add_model_from_file(self, file_path, *model_metadata):
        xmi_file = XMIFile(file_path)
        diagrams = xmi_file.get_diagrams()
        for diagram in diagrams:
            parser = self.factory.get_parser(xmi_file.get_format(), diagram)
            parsed_model = parser.parse_file(file_path, *model_metadata)
            try:
                self.neo4j_manager.delete_model(model_id=parsed_model.id)
                self.neo4j_manager.add_model(parsed_model)
            except:
                print(f'could not parse model from file {file_path}')
                return False
        return True

    def delete_model_from_file(self, file_path):
        xmi_file = XMIFile(file_path)
        diagrams = xmi_file.get_diagrams()
        for diagram in diagrams:
            parser = self.factory.get_parser(xmi_file.get_format(), diagram)
            parsed_model = parser.parse_file(file_path)
            try:
                self.neo4j_manager.delete_model(model_id=parsed_model.id)
            except:
                print(f'could not parse model from file {file_path}')
                return False
        return True

    def add_models_from_github(self, repo_url, owner="", token=""):
        xmi_files = []
        results = []
        get_xmi_files(xmi_files, token, owner, repo_url)
        print(len(xmi_files))
        #download files
        for file_url in xmi_files:
            print(file_url)
            try:
                res = requests.get(file_url)
                file = open("download_file.xml", "w")
                file.write(res.text)
                file.close()
                results.append(self.add_model_from_file("download_file.xml", repo_url, owner))
            except:
                print(f'file download error {file_url}')
        return sum(results), len(xmi_files)

    def delete_models_from_github(self, repo_url, owner="", token=""):
        xmi_files = []
        results = []
        get_xmi_files(xmi_files, token, owner, repo_url)
        print(len(xmi_files))
        #download files
        for file_url in xmi_files:
            print(file_url)
            try:
                res = requests.get(file_url)

                file = open("download_file.xml", "w")
                file.write(res.text)
                file.close()
                results.append(self.delete_model_from_file("download_file.xml"))
            except:
                print(f'file download error {file_url}')
        return sum(results), len(xmi_files)


def create_app():
    settings = ConfigParser()
    neo4j_settings = DEFAULT_CONFIG_FILES[0]
    settings.read(neo4j_settings)
    # TODO - use config file
    neo4j_user = 'neo4j' # settings.get("NEO4J", "USERNAME")
    neo4j_password = 'password' # settings.get("NEO4J", "PASSWORD")
    neo4j_url = 'neo4j:7687'# settings.get("NEO4J", "DATABASE_URL")
    neo4j_cs = f'bolt://{neo4j_user}:{neo4j_password}@{neo4j_url}'
    app = Exquiro(DATABASE_URL=neo4j_cs)
    return app
