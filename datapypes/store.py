from source import Source

class Store(Source):
    __pypes__ = {}

    def save(self, data):
        raise NotImplementedError()

    def update(self, data, **query_model):
        raise NotImplementedError()

    def delete(self, data, **query_model):
        raise NotImplementedError()