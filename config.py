"""Configuration module for the Telegram bot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the bot."""
    
    # Telegram Bot Token (required)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Debug mode
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Railway deployment settings
    PORT = int(os.getenv('PORT', 8000))
    RAILWAY_ENVIRONMENT = os.getenv('RAILWAY_ENVIRONMENT', 'development')
    
    # Security settings
    BOT_OWNER_ID = int(os.getenv('BOT_OWNER_ID', '0'))  # Your Telegram user ID
    ALLOWED_WEBHOOK_IPS = [
        '149.154.160.0/20',   # Telegram webhook IPs
        '91.108.4.0/22',
        '91.108.8.0/22',
        '91.108.12.0/22',
        '91.108.16.0/22',
        '91.108.56.0/22',
        '149.154.160.0/22',
        '149.154.164.0/22',
        '149.154.168.0/22',
        '149.154.172.0/22'
    ]
    
    # Pump.fun URL for scraping
    PUMP_FUN_URL = "https://pump.fun/?coins_sort=created_timestamp&show_animations=false&view=table"
    
    # Request timeout in seconds
    REQUEST_TIMEOUT = 30
    
    # User agent for web scraping
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        return True