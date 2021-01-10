from parsers.ClassDiagramParser import ClassDiagramParser


class ParserFactory:

    @staticmethod
    def get_diagram_dependent_parser(diagram):
        if diagram == 'class_diagram':
            return ClassDiagramParser()
        elif diagram == 'activity_diagram':
            return None
