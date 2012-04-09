from set import Set
from model import Model
from source import Source
from store import Store


class Pype(object):

    @property
    def set(self):
        raise NotImplementedError()

    @property
    def source(self):
        raise NotImplementedError()

    @property
    def store(self):
        raise NotImplementedError()


class SourcePype(Pype):
    def __init__(self, set, source):
        self._set = set
        self._source = source

    # Actions

    def one(self, query_model):
        raise NotImplementedError()
    def latest(self, query_model):
        raise NotImplementedError()
    def search(self, query_model):
        raise NotImplementedError()
    def stream(self, query_model):
        raise NotImplementedError()
    def all(self, query_model):
        raise NotImplementedError()

    # Source action invocation

    def retrieve_model(self, result):
        return self.set.model(**result)

    def retrieve_set(self, results):
        return self.set(*[self.retrieve_model(r) for r in results])


class StorePype(Pype):
    def __init__(self, set, store):
        self._set = set
        self._store = store

    # Actions

    def save(self, data_type):
        return self._store_method('save', data_type)

    def update(self, data_type, query_model=None):
        return self._store_method('update', data_type, query_model)

    def delete(self, data_type, query_model=None):
        return self._store_method('save', data_type, query_model)


    # Define bindings in subclass

    def save_model(self, data_model):
        raise NotImplementedError()

    def save_set(self, data_set):
        raise NotImplementedError()

    def update_model(self, data_model):
        raise NotImplementedError()

    def update_set(self, data_set, query_model):
        raise NotImplementedError()

    def delete_model(self, data_model):
        raise NotImplementedError()

    def delete_set(self, data_set, query_model):
        raise NotImplementedError()

    # Action invocation

    def _store_method(self, method, data_type, query=None):
        if isinstance(data_type, Set):
            method += "_set"
        elif isinstance(data_type, Model):
            method += "_model"
        else:
            raise InvalidPypeDataType(data_type)
        kwargs = {} if query is None else {'query_model': query}
        getattr(self, method)(data_type, **kwargs)
        return self.set


def register_pypes(*pype_classes):
    for cls in pype_classes:
        if hasattr(cls,'__bases__') and StorePype in cls.__bases__:
            Store.__pypes__.setdefault(cls.store,{})[cls.set] = cls
            Store.__pypes__.setdefault(cls.store,{})[cls.set.model] = cls
            Set.__pypes__.setdefault(cls.set,{})[cls.store] = cls
            Model.__pypes__.setdefault(cls.set.model,{})[cls.store] = cls
        elif hasattr(cls,'__bases__') and SourcePype in cls.__bases__:
            Source.__pypes__.setdefault(cls.source,{})[cls.set] = cls
            Source.__pypes__.setdefault(cls.source,{})[cls.set.model] = cls
            Set.__pypes__.setdefault(cls.set,{})[cls.source] = cls
            Model.__pypes__.setdefault(cls.set.model,{})[cls.source] = cls