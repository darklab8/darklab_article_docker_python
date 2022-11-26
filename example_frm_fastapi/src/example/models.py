from sqlalchemy import Column, Integer, String, DateTime
from ..core.base import Model


class Example(Model):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
