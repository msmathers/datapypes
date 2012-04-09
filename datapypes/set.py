from source import Source
from store import Store

class InvalidModelType(Exception): pass
class InvalidSource(Exception): pass
class InvalidStore(Exception): pass
class PypeDoesNotExist(Exception): pass

class Set(object):
    __pypes__ = {}

    def __init__(self, *data, **query):
        self._objects = []
        for obj in data:
            self.add(obj)
        self._query = self.model(**query)
        self._validate()

    def __iter__(self):
        for n in self._objects:
            yield n

    def add(self, obj, validate=False):
        if not isinstance(obj, self.model):
            raise InvalidModelType(obj)
        self._objects.append(obj)
        if validate:
            self._validate()
        return self

    def filter(self, func):
        self._objects = [obj for obj in self if func(obj)]
        return self

    # Validation

    def _validate(self):
        '''Validate entire set'''
        return True

    # Source actions

    def _source_action(self, method, *sources):
        for source in sources:
            if not isinstance(source, Source):
                raise InvalidSource(source)
            pype = self.__pypes__.get(self.__class__,{}).get(source.__class__)
            if pype is None:
                raise PypeDoesNotExist(self.__class__, source.__class__)
            _pype = pype(self, source)
            for obj in getattr(_pype, method)(self._query):
                self.add(obj)
        return self

    def one(self, *sources):
        return self._source_action('one', *sources)
    def latest(self, *sources):
        return self._source_action('latest', *sources)
    def search(self, *sources):
        raise NotImplementedError()
    def stream(self, *sources):
        raise NotImplementedError()
    def all(self, *sources):
        raise NotImplementedError()

    # Store actions

    def _store_action(self, method, *stores):
        for store in stores:
            if not isinstance(store, Store):
                raise InvalidStore(store)
            pype = self.__pypes__.get(self.__class__,{}).get(store.__class__)
            if pype is None:
                raise PypeDoesNotExist(self.__class__, store.__class__)
            _pype = pype(self, store)
            getattr(_pype, method)(self)
        return self

    def save(self, *stores):
        return self._store_action('save', *stores)
    def update(self, *stores):
        raise NotImplementedError()
    def delete(self, *stores):
        raise NotImplementedError()
