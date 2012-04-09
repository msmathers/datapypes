from attribute import Attribute, InvalidAttributeValue
from source import Source
from store import Store

class InvalidAttribute(Exception): pass
class AttributeDoesNotExist(Exception): pass
class InvalidSource(Exception): pass
class InvalidStore(Exception): pass
class PypeDoesNotExist(Exception): pass

class Model(object):
    __pypes__ = {}

    def __init__(self, **attributes):
        self._data = {}
        # Validate model attributes
        for k,v in attributes.items():
            setattr(self, k, v)
        # Nullify missing attributes
        for attr in self._attributes:
            if attr not in self._data:
                setattr(self, attr, None)
        # Validate model
        self._validate()

    def _validate(self):
        return True

    # Attribute validation

    @property
    def _attributes(self):
        #Ensure Model attributes have been registered
        if not hasattr(self.__class__, '__attributes__'):
            self.__class__.__attributes__ = {}
            for k,v in self.__class__.__dict__.items():
                if isinstance(v, Attribute):
                    self.__class__.__attributes__[k] = v
        return self.__class__.__attributes__

    def _validate_attribute(self, attr, val):
        attribute = self._attributes.get(attr)
        if attribute is None:
            raise AttributeDoesNotExist(attr)
        if not attribute._validate(val):
            raise InvalidAttribute(attr, attribute.__class__.__name__, val)
        return True

    def __setattr__(self, attr, value):
        if attr in self._attributes:
            if self._data.get(attr) is None:
                if self._validate_attribute(attr, value):
                    self._data[attr] = value
                    self.__dict__[attr] = value
                else:
                    raise InvalidAttribute(attr, value)
        else:
            self.__dict__[attr] = value

    def _update(self, model):
        for k,v in model._data.items():
            setattr(self, k, v)

    # Source methods

    def get(self, *sources):
        for source in sources:
            if not isinstance(source, Source):
                raise InvalidSource(source)
            pype = self.__pypes__.get(self.__class__,{}).get(source.__class__)
            if pype is None:
                raise PypeDoesNotExist(self.__class__, source.__class__)
            self._update(pype(self, source).one(self))
        return self

    # Store methods

    def _store_action(self, method, *stores):
        for store in stores:
            if not isinstance(store, Store):
                raise InvalidStore(store)
            pype = self.__pypes__.get(self.__class__,{}).get(store.__class__)
            if pype is None:
                raise PypeDoesNotExist(self.__class__, store.__class__)
            getattr(pype(self, store), method)(self)
        return self

    def save(self, *stores):
        return self._store_action('save', *stores)
    def update(self, *stores):
        return self._store_action('update', *stores)
    def delete(self, *stores):
        return self._store_action('delete', *stores)