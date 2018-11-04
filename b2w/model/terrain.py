from b2w.model.base import BaseModel


class Terrain(BaseModel):
    @prperty
    def data(self):
        return {'type': self.type}
