import functools, json
from urllib.parse import urlencode
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.httpclient import HTTPClientError

from b2w.server import make_app


def _data(test_case, test):
    data = test_case.data[test.__name__]
    if type(data) == list:
        return data[0]
    return data


def _route(model):
    return model.collection().name


def database(test):
    @functools.wraps(test)
    async def wrapper(test_case):
        data = _data(test_case, test)
        model = test_case.model
        _id = model.collection().insert_one(data).inserted_id
        await test(test_case, _id)
    return gen_test(wrapper)


class HandlerTestCase:

    def tearDown(self):
        self.model.collection().drop()

    def get_app(self):
       return make_app() 

    @database
    async def test_get_model(self, _id):
        response = await self.request(_id, method='GET')
        self.assertTrue(response.body)

    @gen_test
    async def test_get_nonexistent_model(self):
        error = await self.request('5be0622e08301fc814313d48', method='GET')
        self.assertEqual(404, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_get_with_invalid_id(self):
        error = await self.request('atg1234', method='GET')
        self.assertEqual(404, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_insert_model(self):
        body = self.data['test_insert_model']
        await self.request('', method='POST', body=urlencode(body))
        model = self.model.collection().find_one(body)
        self.assertTrue(model)

    @gen_test
    async def test_insert_without_data(self):
        error = await self.request('', method='POST', body=urlencode({}))
        self.assertEqual(400, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @database
    async def test_update_model(self, _id):
        expected = self.data['test_update_model'][1]
        await self.request(_id, method='POST', body=urlencode(expected))
        model = self.model.collection().find_one({'_id': _id})
        self.assertEqual(expected['name'], model['name'])

    @database
    async def test_update_without_data(self, _id):
        error = await self.request(_id, method='POST', body=urlencode({}))
        self.assertEqual(400, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_update_nonexistent_model(self):
        body = urlencode(self.data['test_update_nonexistent_model'])
        error = await self.request('2de0622e08301fc765313d21', method='POST', body=body)
        self.assertEqual(404, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_update_with_invalid_id(self):
        body = urlencode(self.data['test_update_with_invalid_id'])
        error = await self.request('abc1234', method='POST', body=body)
        self.assertEqual(404, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @database
    async def test_delete_model(self, _id):
        await self.request(_id, method='DELETE')
        model = self.model.collection().find_one({'_id': _id})
        self.assertFalse(model)

    @gen_test
    async def test_delete_nonexistent_model(self):
        error = await self.request('6ce0677e08393fc814313d64', method='DELETE')
        self.assertEqual(404, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_delete_with_invalid_id(self):
        error = await self.request('lnb1235', method='DELETE')
        self.assertEqual(404, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    async def request(self, _id, **kwargs):
        try:
            url = self.get_url('/{0}/{1}'.format(_route(self.model), _id))
            return await self.http_client.fetch(url, **kwargs)
        except HTTPClientError as exception:
            return exception
