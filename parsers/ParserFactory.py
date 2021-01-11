class ParserFactory:

    def __init__(self):
        self._parsers = {}

    def register_parser(self, model_format, diagram, parser):
        if model_format not in self._parsers:
            self._parsers[model_format] = {}
        self._parsers[model_format][diagram] = parser

    def get_parser(self, model_format, diagram):
        parser = self._parsers.get(model_format)
        if not parser or diagram not in parser:
            raise ValueError(model_format, diagram)
        return parser.get(diagram)()
