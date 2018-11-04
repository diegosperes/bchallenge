from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from pymongo import MongoClient
from tornado.ioloop import IOLoop


class BaseModel:

    _client = MongoClient()
    _executor = ThreadPoolExecutor(max_workers=10)

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
