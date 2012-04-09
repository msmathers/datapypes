class Source(object):
    __pypes__ = {}

    def one(self, **query_model):
        raise NotImplementedError()

    def latest(self, **query_model):
        raise NotImplementedError()

    def search(self, **query_model):
        raise NotImplementedError()

    def stream(self, **query_model):
        raise NotImplementedError()

    def all(self, **query_model):
        raise NotImplementedError()