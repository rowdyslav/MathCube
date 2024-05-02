from urllib.parse import quote

from environs import Env

env = Env()
env.read_env()

MONGO_HOST = env.str("MONGO_HOST", "localhost")
MONGO_PORT = env.int("MONGO_PORT", 27017)
MONGO_USER = env.str("MONGO_USER", None)
MONGO_PASS = env.str("MONGO_PASS", None)
MONGO_NAME = env.str("MONGO_NAME", "bot")

MONGO_URL = env.str("MONGO_URL", f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
if MONGO_USER and MONGO_PASS:
    MONGO_URL = (
        f"mongodb://{quote(MONGO_USER)}:{quote(MONGO_PASS)}@{MONGO_HOST}:{MONGO_PORT}/"
    )
