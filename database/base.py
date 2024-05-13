from typing import Literal, Self

from bson import ObjectId
from pymongo.collection import Collection


class Base:
    _collection: Collection

    @classmethod
    def _get(cls, _id: str) -> Self | None:
        obj = cls._collection.find_one({"_id": _id})
        return cls(**obj) if obj else None

    @classmethod
    def _getall(cls) -> list[Self]:
        objs = [cls(**document) for document in cls._collection.find({})]
        return objs

    @classmethod
    def _update(cls, _id: str, operation: Literal["$set", "$inc"], **kwargs) -> None:
        cls._collection.find_one_and_update({"_id": _id}, {operation: kwargs})

    @classmethod
    def _create(cls, **kwargs) -> Self:
        fields = {
            "_id": str(ObjectId()),
            "statistic": {
                category: {"correct": 0, "all": 0}
                for category in ("sample", "quadratic_equation")
            },
            **kwargs,
        }
        cls._collection.insert_one(fields)
        return cls(**fields)

    @classmethod
    def _delete(cls, _id: str) -> None:
        cls._collection.find_one_and_delete({"_id": _id})

    @classmethod
    def set_collection(cls, сollection: Collection) -> None:
        cls._collection = сollection
