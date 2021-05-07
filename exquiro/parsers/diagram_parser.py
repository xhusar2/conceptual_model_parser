from exquiro.models.model import Model


class DiagramParser:
    """Model base class."""
    # abstract methods
    def parse_file(self, file_path) -> Model:
        """Returns parsed model"""
        pass
