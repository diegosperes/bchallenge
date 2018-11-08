import json
import ast
from tornado.web import RequestHandler
from bson.objectid import ObjectId
from bson.errors import InvalidId
from bson import json_util
from b2w import uri


def normalize(data):
    return data[0] if len(data) == 1 else data


class Handler(RequestHandler):

    @property
    def model(self):
        raise NotImplementedError()

    @property
    def data(self):
        body = self.request.body.decode()
        try:
            return json.loads(body)
        except json.decoder.JSONDecodeError:
            pass

        try:
            return ast.literal_eval(body)
        except (ValueError, SyntaxError):
            pass

        return {key: normalize(self.get_arguments(key))
                for key in self.request.arguments}

    async def get(self, _id):
        self.set_header('Content-Type', 'application/json')
        model = await self._find(_id)
        if model:
            data = model.data
            data['id'] = _id
            self.finish(data)
        elif not _id:
            await self._list()
        else:
            self._not_found()

    async def post(self, _id):
        self.set_header('Content-Type', 'application/json')
        if self.data and _id:
            await self._update(_id)
        elif self.data:
            model = self.model(**self.data)
            await model.insert()
        else:
            self._bad_request()

    async def delete(self, _id):
        self.set_header('Content-Type', 'application/json')
        model = await self._find(_id)
        if model:
            await model.delete()
        else:
            self._not_found()

    async def _list(self):
        result = {}
        page = self._get_page()
        name = self.get_argument('name', None)
        result['result'] = await self.model.list(page, name=name)
        if len(result['result']) == self.model.LIMIT:
            result['next'] = uri(self.model, None, page=page + 1)
        if page > 1:
            result['previous'] = uri(self.model, None, page=page - 1)
        self.finish(json_util.dumps(result))

    async def _update(self, _id):
        model = await self._find(_id)
        if model:
            for key, value in self.data.items():
                setattr(model, key, value)
            await model.update()
        else:
            return self._not_found()

    async def _find(self, _id):
        try:
            return await self.model.find(_id=ObjectId(_id))
        except (TypeError, InvalidId):
            pass

    def _get_page(self):
        page = normalize(self.get_argument('page', [1]))
        try:
            return int(page)
        except ValueError:
            return 0

    def _not_found(self):
        self.set_status(404)
        self.finish({})

    def _bad_request(self):
        self.set_status(400)
        self.finish({})
