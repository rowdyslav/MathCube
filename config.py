from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
MONGO_URI = env.str("MONGO_URI")
