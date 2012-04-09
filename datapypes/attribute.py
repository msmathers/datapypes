class InvalidAttributeValue(Exception): pass

class Attribute(object):
    def __init__(self, **properties):
        self._properties = properties
    def _validate(self, val):
        return False