from b2w.handler.base import Handler
from b2w.model.terrain import Terrain


class TerrainHandler(Handler):

    @property
    def model(self):
        return Terrain
