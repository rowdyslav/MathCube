from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel


# TODO
class Base(BaseModel):
    _collection = None

    @classmethod
    async def count(cls):
        num = await cls._collection.count_documents({})
        return num

    @classmethod
    async def get(cls, id: int):
        obj = await cls._collection.find_one({"_id": id})
        return cls(**obj) if obj else None

    @classmethod
    async def get_all(cls):
        objs = cls._collection.find()
        return [cls(**obj) async for obj in objs]

    @classmethod
    async def update(cls, id: int, **kwargs):
        await cls._collection.find_one_and_update({"_id": id}, {"$set": kwargs})
        return await cls.get(id)

    @classmethod
    async def create(cls, **kwargs):
        if "_id" not in kwargs:
            kwargs["_id"] = await cls.count() + 1
        obj = cls(**kwargs)
        obj = await cls._collection.insert_one(obj.model_dump(by_alias=True))
        return await cls.get(obj.inserted_id)

    @classmethod
    async def delete(cls, id: int):
        await cls._collection.find_one_and_delete({"_id": id})
        return True
