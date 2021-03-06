from neomodel import config
from neomodel import db as neo_db

# this class represents Neo4j manager. It stores model to db, deletes models from db, executes queries.
class Neo4jManager():

    def __init__(self, DATABASE_URL):
        config.DATABASE_URL = DATABASE_URL
        config.ENCRYPTED_CONNECTION = False

    @staticmethod
    def delete_all():
        neo_db.cypher_query("MATCH ()-[r]-() DETACH DELETE r")
        neo_db.cypher_query("MATCH (n) DETACH DELETE n")
        return True
    @staticmethod
    def delete_model(model_id):
        neo_db.cypher_query(f'MATCH (n)-[r]-() WHERE n.model_id = \'{model_id}\' DETACH DELETE r')
        neo_db.cypher_query(f'MATCH (n) WHERE n.model_id = \'{model_id}\' DETACH DELETE n')
        return True

    @staticmethod
    def add_model(model):
        nodes, relations = model.get_neo4j_model()
        _nodes = {}
        for node_id, node in nodes.items():
            node.save()
        for r in relations:
            rel_source = r[0]
            rel_dest = r[1]
            rel_props = r[2]
            rel_attrib = r[3]
            if rel_source in nodes and rel_dest in nodes:
                src = nodes[rel_source]
                dest = nodes[rel_dest]
                getattr(src, rel_attrib).connect(dest, rel_props)
        return True


