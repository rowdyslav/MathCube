from urllib.parse import quote

from environs import Env

env = Env()
env.read_env()

MONGO_URL = env.str("MONGO_URL")
