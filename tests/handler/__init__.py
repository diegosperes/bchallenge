import functools
import json
import logging
import pymongo
from urllib.parse import urlencode
from tornado.testing import gen_test
from tornado.httpclient import HTTPClientError
from tornado.options import options

from b2w.server import make_app

logging.getLogger("tornado.access").setLevel(logging.CRITICAL)


def create(names, test_case):
    _ids = []
    for name in names:
        data = test_case.factory(name)
        _id = test_case.model.collection().insert_one(data).inserted_id
        _ids.append(_id)
    return _ids


def database(name, many=False):
    def wrapper(test):
        @functools.wraps(test)
        async def _wrapp(test_case):
            _ids = create(wrapper.names, test_case)
            await test(test_case, _ids)
        return gen_test(_wrapp)
    suffixes = 'abcdefghijklm' if many else ' '
    wrapper.names = [name + suffix for suffix in suffixes]
    return wrapper


class HandlerTestCase:

    def tearDown(self):
        self.model.collection().drop()

    def get_app(self):
        return make_app()

    @database('Black')
    async def test_get_model(self, _ids):
        response = await self.request(_ids[0], method='GET')
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
        body = self.factory('Blue')
        await self.request('', method='POST', body=urlencode(body))
        model = self.model.collection().find_one({"name": body['name']})
        self.assertTrue(model)

    @gen_test
    async def test_insert_without_data(self):
        error = await self.request('', method='POST', body=urlencode({}))
        self.assertEqual(400, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @database('Green')
    async def test_update_model(self, _ids):
        expected = self.factory('Purple')
        await self.request(_ids[0], method='POST', body=urlencode(expected))
        model = self.model.collection().find_one({'_id': _ids[0]})
        self.assertEqual(expected['name'], model['name'])

    @database('Orange')
    async def test_update_without_data(self, _ids):
        error = await self.request(_ids[0], method='POST', body=urlencode({}))
        self.assertEqual(400, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_update_nonexistent_model(self):
        body = urlencode(self.factory('Pink'))
        error = await self.request('2de0622e08301fc765313d21', method='POST', body=body)
        self.assertEqual(404, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_update_with_invalid_id(self):
        body = urlencode(self.factory('Brown'))
        error = await self.request('abc1234', method='POST', body=body)
        self.assertEqual(404, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @database('Red')
    async def test_delete_model(self, _ids):
        await self.request(_ids[0], method='DELETE')
        model = self.model.collection().find_one({'_id': _ids[0]})
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

    @gen_test
    async def test_get_empty_list(self):
        response = await self.request('', method='GET')
        self.assertEqual(b'{"result": [], "next": null, "previous": null}', response.body)

    @database('White')
    async def test_get_first_page_with_invalid_page_value(self, _ids):
        response = await self.request('?page=a', method='GET')
        result = json.loads(response.body)
        self.assertEqual(1, len(result['result']))
        route = self.model.collection().name
        expected = '{0}/{1}/{2}'.format(options.host, route, _ids[0])
        self.assertEqual(expected, result['result'][0]['uri'])

    @database('White snow', many=True)
    async def test_get_list_without_page(self, _ids):
        response = await self.request('', method='GET')
        result = json.loads(response.body)
        self.assertEqual(10, len(result['result']))

    @database('Silver', many=True)
    async def test_get_zero_page(self, _ids):
        response = await self.request('?page=0', method='GET')
        result = json.loads(response.body)
        self.assertEqual(10, len(result['result']))

    @database('Gray', many=True)
    async def test_get_first_page(self, _ids):
        response = await self.request('?page=1', method='GET')
        result = json.loads(response.body)
        self.assertEqual(10, len(result['result']))

    @database('Yellow', many=True)
    async def test_get_second_page(self, _ids):
        response = await self.request('?page=2', method='GET')
        result = json.loads(response.body)
        self.assertEqual(3, len(result['result']))

    @database('Space Gray', many=True)
    async def test_show_next_page(self, _ids):
        response = await self.request('?page=1', method='GET')
        result = json.loads(response.body)
        route = self.model.collection().name
        expected = '{0}/{1}?page=2'.format(options.host, route)
        self.assertEqual(expected, result['next'])

    @database('Ocean Blue', many=True)
    async def test_show_previous_page(self, _ids):
        response = await self.request('?page=2', method='GET')
        result = json.loads(response.body)
        route = self.model.collection().name
        expected = '{0}/{1}?page=1'.format(options.host, route)
        self.assertEqual(expected, result['previous'])

    @database('Dark matter')
    async def test_search_by_name(self, _ids):
        self.model.collection().create_index([('name', pymongo.TEXT)])
        response = await self.request('?name=matter', method='GET')
        result = json.loads(response.body)
        self.assertEqual(1, len(result['result']))

    async def request(self, _id, **kwargs):
        try:
            route = self.model.collection().name
            url = self.get_url('/{0}/{1}'.format(route, _id))
            return await self.http_client.fetch(url, **kwargs)
        except HTTPClientError as exception:
            return exception
