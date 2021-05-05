class Model:
    """Model base class. Consists of nodes and relations which are ready to by inserted to Neo4j"""

    def __init__(self, *model_metadata):
        self.model_metadata = model_metadata

    # abstract methods
    def get_neo4j_model(self):
        """Returns nodes and relations in 2 separate lists."""
        pass
