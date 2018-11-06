import ast
from b2w.model.base import BaseModel


class Planet(BaseModel):

    @property
    def data(self):
        return {'name': self.name, 'climate': self.climate, 'terrain': self.terrain, 'movie': self.movie}

    def __init__(self, **kwargs):
        kwargs['climate'] = self._normalize(kwargs, 'climate')
        kwargs['movie'] = self._normalize(kwargs, 'movie')
        kwargs['terrain'] = self._normalize(kwargs, 'terrain')
        super().__init__(**kwargs)

    def _normalize(self, kwargs, key):
        value = kwargs.get(key, '[]')
        return ast.literal_eval(value) if type(value) is str else value
