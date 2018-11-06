from b2w.handler.base import Handler
from b2w.model.planet import Planet
from bson.errors import InvalidId


class PlanetHandler(Handler):

    @property
    def model(self):
        return Planet

    async def post(self, _id):
        try:
            await super().post(_id)
        except InvalidId:
            self._bad_request()
