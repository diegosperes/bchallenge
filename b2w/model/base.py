from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from pymongo import MongoClient
from bson import json_util
from tornado.ioloop import IOLoop


def serialize(model, document):
    data = model(**document).data
    data['id'] = str(document['_id'])
    return data


class BaseModel:

    _client = MongoClient()
    _executor = ThreadPoolExecutor(max_workers=10)
    LIMIT = 10

    @classmethod
    def database(cls):
        return 'star_wars'

    @classmethod
    def collection(cls):
        database = cls.database()
        collection = cls.__name__.lower()
        return cls._client[database][collection]

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value) 

    @classmethod
    async def find(cls, **query):
        def _find(collection, query):
            return collection.find_one(query)
        document = await cls._run(_find, query)
        return cls(**document)

    @classmethod
    async def list(cls, page):
        def _list(collection, skip, limit):
            cursor = collection.find()
            cursor.skip(skip).limit(limit).sort('_id')
            return [serialize(cls, document) for document in cursor]
        skip = (page - 1) * cls.LIMIT if page > 0 else 0
        return await cls._run(_list, skip, cls.LIMIT)

    async def insert(self):
        def _insert(collection, data):
            return collection.insert_one(data)
        self._id = (await self._run(_insert, self.data)).inserted_id

    async def update(self):
        query = {'_id': self._id}
        def _update(collection, query, data):
            data = {'$set': data}
            return collection.update_one(query, data)
        return await self._run(_update, query, self.data)

    async def delete(self):
        query = {'_id': self._id}
        def _delete(collection, query):
            return collection.delete_one(query)
        return await self._run(_delete, query)
    
    @classmethod
    async def _run(cls, function, *args):
        ioloop = IOLoop.current()
        return await ioloop.run_in_executor(cls._executor, function, cls.collection(), *args)
