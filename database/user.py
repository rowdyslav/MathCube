from pydantic import Field

from .base import Base


class User(Base):
    id: int = Field(default_factory=int, alias="_id")
    username: str | None = Field(default=None)

    @classmethod
    async def get_or_create(cls, id: int, username: str | None):
        user = await cls.get(id)
        user = (
            await cls.update(user.id, username=username)
            if user
            else await cls.create(_id=id, username=username)
        )
        return user


User.set_collection("users")
