"""Main Telegram bot implementation."""

import logging
import asyncio
from datetime import datetime
from typing import List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    ContextTypes,
    MessageHandler,
    filters
)
from telegram.constants import ParseMode

from config import Config
from scraper import PumpFunScraper, CoinData

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not Config.DEBUG else logging.DEBUG
)
logger = logging.getLogger(__name__)

class PumpFunBot:
    """Telegram bot for displaying pump.fun coin data."""
    
    def __init__(self):
        self.scraper = PumpFunScraper()
        self.last_update_time = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command."""
        welcome_message = (
            "🚀 **Pump.fun New Coins Bot** 🚀\n\n"
            "Welcome! This bot shows you the top 5 newest coins from pump.fun.\n\n"
            "**Commands:**\n"
            "• /start - Show this welcome message\n"
            "• /refresh - Get the latest new coins\n"
            "• /help - Show help information\n\n"
            "Click the **🔄 Refresh** button below to get started!"
        )
        
        keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /help command."""
        help_message = (
            "📖 **Help - Pump.fun New Coins Bot**\n\n"
            "This bot fetches and displays the top 5 newest coins from pump.fun.\n\n"
            "**Available Commands:**\n"
            "• `/start` - Show welcome message and refresh button\n"
            "• `/refresh` - Get the latest new coins data\n"
            "• `/help` - Show this help message\n\n"
            "**How to use:**\n"
            "1. Click the 🔄 Refresh button to fetch latest data\n"
            "2. The bot will show coin information including:\n"
            "   • Coin name and symbol\n"
            "   • Current price\n"
            "   • Market cap\n"
            "   • 24h price change\n"
            "   • Trading volume\n\n"
            "**Note:** Data is fetched live from pump.fun and may take a few seconds to load.\n\n"
            "Need more coins? Just click refresh again! 🚀"
        )
        
        keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def refresh_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /refresh command."""
        await self._send_coin_data(update, context, is_callback=False)
    
    async def refresh_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle refresh button callback."""
        query = update.callback_query
        await query.answer()  # Acknowledge the button press
        
        await self._send_coin_data(update, context, is_callback=True)
    
    async def _send_coin_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False) -> None:
        """Fetch and send coin data to user."""
        try:
            # Show loading message
            loading_message = "🔄 Fetching the latest coins from pump.fun..."
            
            if is_callback:
                # Edit the existing message for callback
                await update.callback_query.edit_message_text(
                    loading_message,
                    parse_mode=ParseMode.MARKDOWN
                )
                chat_id = update.callback_query.message.chat_id
                message_id = update.callback_query.message.message_id
            else:
                # Send new message for command
                loading_msg = await update.message.reply_text(
                    loading_message,
                    parse_mode=ParseMode.MARKDOWN
                )
                chat_id = loading_msg.chat_id
                message_id = loading_msg.message_id
            
            # Fetch coin data
            logger.info("Fetching coin data...")
            coins = await self._fetch_coins_async()
            
            if not coins:
                error_message = (
                    "❌ **Error fetching coin data**\n\n"
                    "Unable to fetch coin data from pump.fun right now. "
                    "This could be due to:\n"
                    "• Website being temporarily unavailable\n"
                    "• Network connectivity issues\n"
                    "• Site structure changes\n\n"
                    "Please try again in a few moments."
                )
                keyboard = [[InlineKeyboardButton("🔄 Try Again", callback_data="refresh")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=error_message,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
                return
            
            # Format the message
            message = self._format_coins_message(coins)
            
            # Create refresh button
            keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Update the message with coin data
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
            self.last_update_time = datetime.now()
            logger.info(f"Successfully sent data for {len(coins)} coins")
            
        except Exception as e:
            logger.error(f"Error in _send_coin_data: {e}")
            
            error_message = (
                "❌ **Unexpected Error**\n\n"
                "An unexpected error occurred while fetching coin data. "
                "Please try again later or contact support if the problem persists."
            )
            keyboard = [[InlineKeyboardButton("🔄 Try Again", callback_data="refresh")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                if is_callback:
                    await update.callback_query.edit_message_text(
                        error_message,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup
                    )
                else:
                    await context.bot.edit_message_text(
                        chat_id=update.message.chat_id,
                        message_id=message_id,
                        text=error_message,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=reply_markup
                    )
            except Exception as edit_error:
                logger.error(f"Error editing message: {edit_error}")
                # As last resort, send a new message
                await update.effective_chat.send_message(
                    error_message,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
    
    async def _fetch_coins_async(self) -> List[CoinData]:
        """Fetch coins asynchronously."""
        loop = asyncio.get_event_loop()
        try:
            # Run the scraper in a thread pool to avoid blocking
            coins = await loop.run_in_executor(None, self.scraper.fetch_new_coins)
            return coins
        except Exception as e:
            logger.error(f"Error fetching coins: {e}")
            return []
    
    def _format_coins_message(self, coins: List[CoinData]) -> str:
        """Format the list of coins into a Telegram message."""
        if not coins:
            return "❌ No coins found"
        
        header = (
            "🚀 **Top 5 New Coins from Pump.fun** 🚀\n"
            f"📅 Updated: {datetime.now().strftime('%H:%M:%S UTC')}\n\n"
        )
        
        coin_messages = []
        for i, coin in enumerate(coins, 1):
            coin_msg = (
                f"**{i}. {coin.name}** (`{coin.symbol}`)\n"
                f"💵 Price: `{coin.price}`\n"
                f"📊 Market Cap: `{coin.market_cap}`\n"
                f"{'🟢' if not coin.change_24h.startswith('-') else '🔴'} 24h: `{coin.change_24h}`\n"
                f"📈 Volume: `{coin.volume_24h}`\n"
            )
            coin_messages.append(coin_msg)
        
        # Join all coin messages
        coins_text = "\n".join(coin_messages)
        
        footer = (
            "\n📊 **Data Source:** pump.fun\n"
            "🔄 Click refresh for latest data\n"
            "⚠️ *Always DYOR before investing*"
        )
        
        full_message = header + coins_text + footer
        
        # Telegram has a 4096 character limit for messages
        if len(full_message) > 4000:
            # Truncate if too long and add notice
            truncated = full_message[:3900] + "\n\n... *Message truncated*"
            return truncated
        
        return full_message
    
    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle unknown messages."""
        message = (
            "❓ **Unknown Command**\n\n"
            "I didn't understand that command. Here's what I can do:\n\n"
            "• `/start` - Get started with the bot\n"
            "• `/refresh` - Get latest coin data\n"
            "• `/help` - Show detailed help\n\n"
            "Or just click the refresh button below! 👇"
        )
        
        keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    def setup_handlers(self, app: Application) -> None:
        """Set up command and callback handlers."""
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("refresh", self.refresh_command))
        app.add_handler(CallbackQueryHandler(self.refresh_callback, pattern="refresh"))
        
        # Handle unknown text messages
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.unknown_command))

def main():
    """Main function to run the bot."""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}")
        print("Please make sure you have set up your .env file with TELEGRAM_BOT_TOKEN")
        return
    
    # Create application
    app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    # Create bot instance and setup handlers
    bot = PumpFunBot()
    bot.setup_handlers(app)
    
    # Start the bot
    logger.info("Starting Pump.fun Telegram Bot...")
    print("🚀 Pump.fun Telegram Bot is starting...")
    print("Press Ctrl+C to stop the bot")
    
    # Run the bot with proper error handling
    try:
        app.run_polling()
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        print(f"Error: {e}")