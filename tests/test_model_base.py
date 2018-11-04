from tornado.testing import AsyncTestCase, gen_test
from b2w.model.base import BaseModel


class Staff(BaseModel):
    @classmethod
    def database(cls):
        return 'test_database'

    @property
    def data(self):
        return {'name': self.name}


class BaseModelTestCase(AsyncTestCase):

    def setUp(self):
        super().setUp()
        name = 'Diego'
        self.collection = Staff.collection()
        self.collection.insert_one({'name': name})
        self.document = self.collection.find_one({'name': name})

    def tearDown(self):
        self.collection.drop()

    def test_get_collection(self):
        self.assertEqual('staff', self.collection.name)
    
    @gen_test
    async def test_find(self):
        model = await Staff.find(name=self.document['name'])
        self.assertIsInstance(model, Staff)
        self.assertEqual(self.document['name'], model.name)
        self.assertTrue(model._id)

    @gen_test
    async def test_insert(self):
        model = Staff(name='Felipe')
        await model.insert()
        document = self.collection.find_one({'name': model.name})
        self.assertEqual({'name': model.name, '_id': document['_id']}, document)
        self.assertTrue(model._id)

    @gen_test
    async def test_update(self):
        staff = Staff(**self.document)
        staff.name = 'Caroline'
        await staff.update()
        updated = self.collection.find_one({'_id': self.document['_id']})
        self.assertEqual({'name': 'Caroline', '_id': staff._id}, updated)

    @gen_test
    async def test_delete(self):
        staff = Staff(**self.document)
        await staff.delete()
        deleted = self.collection.find_one({'_id': self.document['_id']})
        self.assertEqual(None, deleted)
