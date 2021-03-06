import ast
from bson.objectid import ObjectId
from b2w.model.base import BaseModel, serialize
from b2w.model.movie import Movie
from b2w import uri


def lookup(query):
    return [
        {"$match": query},
        {"$unwind": {"path": "$movie", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"movie": {"$toObjectId": "$movie"}}},
        {
            "$lookup": {
                "from": "movie",
                "localField": "movie",
                "foreignField": "_id",
                "as": "movie"
             }
        },
        {"$unwind": {"path": "$movie", "preserveNullAndEmptyArrays": True}},
        {
             "$group": {
                 "_id": "$_id",
                 "name": {"$first": "$name"},
                 "climate": {"$first": "$climate"},
                 "terrain": {"$first": "$terrain"},
                 "movie": {"$push": "$movie"},
             }
         },
    ]


class Planet(BaseModel):

    @property
    def data(self):
        return {
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain,
            'movie': self.movie
        }

    @classmethod
    async def find(cls, **query):
        def _aggregate(collection, query):
            try:
                return collection.aggregate(query).next()
            except StopIteration:
                pass
        document = await cls._run(_aggregate, lookup(query))
        return cls(**document)

    @classmethod
    async def list(cls, page, **kwargs):
        planets = await super().list(page, **kwargs)
        for planet in planets:
            for index, movie in enumerate(planet['movie']):
                planet['movie'][index] = str(movie)
        return planets

    def __init__(self, **kwargs):
        kwargs['climate'] = self._normalize(kwargs, 'climate')
        kwargs['movie'] = self._normalize(kwargs, 'movie', model=Movie)
        kwargs['terrain'] = self._normalize(kwargs, 'terrain')
        super().__init__(**kwargs)
        self._validate()

    def _normalize(self, kwargs, key, model=None):
        value = kwargs.get(key, [])
        value = ast.literal_eval(value) if type(value) is str else value
        normalized = []
        for item in value:
            if type(item) is dict:
                item['uri'] = uri(model, item['_id'])
                item['id'] = str(item['_id'])
                del item['_id']
            normalized.append(item)
        return normalized

    def _validate(self):
        for value in self.movie:
            if type(value) is not dict:
                ObjectId(value)
