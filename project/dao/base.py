from typing import Dict, Any


class BaseDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        raise NotImplemented

    def get_one(self, id: int):
        raise NotImplemented

    def update(self, id: int, data: Dict[str, Any]):
        raise NotImplemented

    def create(self, data: Dict[str, Any]):
        raise NotImplemented

    def delete(self, id: int):
        raise NotImplemented


class DataBaseDAO(BaseDAO):
    def __init__(self, session):
        self.session = session