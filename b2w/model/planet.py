import ast
from bson.objectid import ObjectId
from b2w.model.base import BaseModel


class Planet(BaseModel):

    @property
    def data(self):
        return {
            'name': self.name,
            'climate': [str(climate) for climate in self.climate],
            'terrain': [str(terrain) for terrain in self.terrain],
            'movie': [str(movie) for movie in self.movie]
        }

    def __init__(self, **kwargs):
        kwargs['climate'] = self._normalize(kwargs, 'climate')
        kwargs['movie'] = self._normalize(kwargs, 'movie')
        kwargs['terrain'] = self._normalize(kwargs, 'terrain')
        super().__init__(**kwargs)
        self._validate()

    def _normalize(self, kwargs, key):
        value = kwargs.get(key, '[]')
        return ast.literal_eval(value) if type(value) is str else value

    def _validate(self):
        [ObjectId(_id) for _id in self.movie]
