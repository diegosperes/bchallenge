from b2w.model.base import BaseModel


class Climate(BaseModel):
    @property
    def data(self):
        return {'name': self.name}
