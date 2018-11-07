import json
from tornado.testing import gen_test
from b2w.model.base import BaseModel


class ModelTestCase:

    def setUp(self):
        super().setUp()
        name = 'Blue'
        self.model.database = lambda: 'test_database'
        self.collection = self.model.collection()
        self.collection.insert_one(self.factory(name))
        self.document = self.collection.find_one({'name': name})

    def tearDown(self):
        self.collection.drop()

    @gen_test
    async def test_list(self):
        for letter in 'abcdefghijklm':
            self.collection.insert_one({'name': letter})
        documents = (await self.model.list(0))
        self.assertEqual(10, len(documents))

    @gen_test
    async def test_list_first_page(self):
        for letter in 'abcdefghijklm':
            self.collection.insert_one({'name': letter})
        documents = (await self.model.list(1))
        self.assertEqual(10, len(documents))

    @gen_test
    async def test_list_second_page(self):
        for letter in 'abcdefghijklm':
            self.collection.insert_one({'name': letter})
        documents = (await self.model.list(2))
        self.assertEqual(4, len(documents))

    @gen_test
    async def test_find(self):
        model = await self.model.find(name=self.document['name'])
        self.assertIsInstance(model, self.model)
        self.assertEqual(self.document['name'], model.name)
        self.assertTrue(model._id)

    @gen_test
    async def test_insert(self):
        expected = self.factory('Red')
        model = self.model(**expected)
        await model.insert()
        document = self.collection.find_one({'name': model.name})
        expected['_id'] = document['_id']
        self.assertEqual(expected, document)
        self.assertTrue(model._id)

    @gen_test
    async def test_update(self):
        model = self.model(**self.document)
        model.name = 'White'
        await model.update()
        updated = self.collection.find_one({'_id': self.document['_id']})
        self.document['name'] = model.name
        self.assertEqual(self.document, updated)

    @gen_test
    async def test_delete(self):
        model = self.model(**self.document)
        await model.delete()
        deleted = self.collection.find_one({'_id': self.document['_id']})
        self.assertEqual(None, deleted)
