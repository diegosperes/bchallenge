from b2w.model.base import BaseModel


class Climate(BaseModel):
    @property
    def data(self):
        return {'type': self.type}
