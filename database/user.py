from dataclasses import dataclass
from typing import Self

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .base import Base


@dataclass
class User(UserMixin, Base):
    _id: str
    username: str
    password: str
    statistic: dict[str, dict[str, int]]

    def get_id(self):
        return self._id

    @classmethod
    def signup(cls, username: str, password: str) -> Self | str:
        registered = bool(cls._collection.find_one({"username": username}))
        if registered:
            return "Никнейм уже занят! Попробуйте другой"

        user = cls._create(username=username, password=generate_password_hash(password))
        return user

    @classmethod
    def login(cls, username: str, password: str) -> Self | str:
        user = cls._collection.find_one({"username": username})
        if not user or not check_password_hash(user["password"], password):
            return "Неверный никнейм или пароль!"
        return cls._get(user["_id"])  # type: ignore


from main import app

from .loader import db

with app.app_context():
    User.set_collection(db.users)
