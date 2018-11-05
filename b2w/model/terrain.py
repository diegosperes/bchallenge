from b2w.model.base import BaseModel


class Terrain(BaseModel):
    @property
    def data(self):
        return {'name': self.name}
