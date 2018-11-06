import ast

from b2w.handler.base import Handler
from b2w.model.planet import Planet
from bson.objectid import ObjectId
from bson.errors import InvalidId


class PlanetHandler(Handler):

    @property
    def model(self):
        return Planet
