#   utils/config.py

import os

class Config:
    #   Database configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/sg_bridgeBot')
    
    #   Telegram bot token
    # TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN',
    #                                'your-bot-token-here')
