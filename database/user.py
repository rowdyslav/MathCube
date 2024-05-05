from pydantic import Field

from .base import Base


class User(Base):
    id: int = Field(default_factory=int, alias="_id")
    username: str | None = Field(default=None)

    @classmethod
    async def create(cls, username: str, password):
        user = cls.create(username=username, password=password)
        return user


# User.set_collection("users") TODO
