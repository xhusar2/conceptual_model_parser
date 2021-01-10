
class ParserMeta(type):
    """A Parser metaclass that will be used for parser class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'parse_model') and
                callable(subclass.parse_model) and
                hasattr(subclass, 'parse_file') and
                callable(subclass.parse_file))


class ParserInterface(metaclass=ParserMeta):
    pass
