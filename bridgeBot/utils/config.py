# utils/config.py
import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/sg_bridgebot')
