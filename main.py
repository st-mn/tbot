#!/usr/bin/env python3
"""
Pump.fun Telegram Bot

A Telegram bot that displays the top 10 newest coins from pump.fun
with a refresh button for real-time updates.

Usage:
    python main.py

Make sure to set up your .env file with TELEGRAM_BOT_TOKEN before running.
"""

import asyncio
import sys
import signal
import logging
from bot import main

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\n🛑 Shutting down bot...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Run the bot
        main()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)