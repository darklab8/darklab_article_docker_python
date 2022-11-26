from utils.database.sql import DatabaseFactoryBase, SettingStub

from . import settings


class DatabaseFactory(DatabaseFactoryBase):
    settings = settings  # type: ignore