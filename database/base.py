from typing import Self

from bson import ObjectId
from pymongo.collection import Collection


class Base:
    _collection: Collection

    @classmethod
    def _get(cls, _id: str) -> Self | None:
        obj = cls._collection.find_one({"_id": _id})
        return cls(**obj) if obj else None

    @classmethod
    def _update(cls, _id: str, **kwargs) -> None:
        cls._collection.find_one_and_update({"_id": _id}, {"$set": kwargs})

    @classmethod
    def _create(cls, **kwargs) -> Self:
        obj = cls._collection.insert_one({"_id": str(ObjectId()), **kwargs})
        return cls._get(obj.inserted_id)  # type: ignore

    @classmethod
    def _delete(cls, _id: str) -> None:
        cls._collection.find_one_and_delete({"_id": _id})

    @classmethod
    def set_collection(cls, сollection: Collection) -> None:
        cls._collection = сollection
