from motor.motor_tornado import MotorClient

from config import MONGO_NAME, MONGO_URL

client = MotorClient(MONGO_URL)
db = client[MONGO_NAME]
