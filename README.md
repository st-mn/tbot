# Pump.fun Telegram Bot 🚀

A Python Telegram bot that fetches and displays the top 5 newest coins from [pump.fun](https://pump.fun) with real-time refresh functionality.

## 🤖 Live Bot

**Try it now:** [@PumpingTbot](https://t.me/PumpingTbot) on Telegram

Click the link above or search for `@PumpingTbot` in Telegram to start using the bot!

## � Visual Assets

Bot profile pictures and favicons are available in the [`assets/`](./assets/) directory:
- 🚀 **Bot Profile Picture**: High-res rocket design for Telegram
- 🌐 **Favicon**: Web icon for repository and sites
- 📱 **Multiple Formats**: SVG (scalable) and conversion tools

## �🎯 Quick Start

**Just want to use the bot?** Go to [@PumpingTbot](https://t.me/PumpingTbot) and start chatting!

**Want to run your own instance?** Follow the installation guide below.

## Features ✨

- **Real-time Data**: Fetches the latest new coins from pump.fun
- **Interactive Interface**: Refresh button for instant updates
- **Rich Information**: Shows coin name, symbol, price, market cap, 24h change, and volume
- **Error Handling**: Robust error handling with user-friendly messages
- **Clean UI**: Well-formatted messages with emojis and markdown

## Prerequisites 📋

- Python 3.8 or higher
- A Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather))
- Internet connection for fetching coin data

## Installation 🔧

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd tbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file and add your Telegram Bot Token:
   ```env
   TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
   DEBUG=False
   ```

### 4. Get a Telegram Bot Token

1. Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow the instructions
3. Choose a name for your bot (e.g., "Pump Fun Coins")
4. Choose a username (e.g., "pumpfun_coins_bot")
5. Copy the token provided by BotFather
6. Paste it in your `.env` file

## Usage 🚀

### Starting the Bot

```bash
python main.py
```

You should see output like:
```
🚀 Pump.fun Telegram Bot is starting...
Press Ctrl+C to stop the bot
```

### Bot Commands

Once the bot is running, users can interact with it using:

- `/start` - Welcome message and refresh button
- `/refresh` - Get the latest coin data
- `/help` - Show detailed help information
- **🔄 Refresh Button** - Click to refresh coin data

### Example Output

```
🚀 Top 5 New Coins from Pump.fun 🚀
📅 Updated: 14:30:25 UTC

1. PEPE2.0 (PEPE)
💵 Price: $0.00012
📊 Market Cap: $1.2M
🟢 24h: +15.6%
📈 Volume: $450K

2. DogeCoin Fork (DOGE2)
💵 Price: $0.000089
📊 Market Cap: $890K
🔴 24h: -2.3%
📈 Volume: $230K

... (up to 5 coins)
```

## Project Structure 📁

```
tbot/
├── 📁 Core Application Files
│   ├── main.py                    # Entry point with signal handling
│   ├── bot.py                     # Telegram bot logic with security integration
│   ├── scraper.py                 # pump.fun web scraping functionality
│   ├── config.py                  # Configuration management with security settings
│   └── security.py                # 🆕 Security monitoring and protection system
│
├── 📁 Configuration & Environment
│   ├── .env                       # Your environment variables (TOKEN, etc.)
│   ├── .env.example               # Environment variables template
│   ├── requirements.txt           # Python dependencies
│   └── .gitignore                 # Git ignore rules (includes security files)
│
├── 📁 Deployment & Infrastructure
│   ├── Dockerfile                 # Docker container configuration
│   ├── Procfile                   # Railway deployment process file
│   └── DEPLOY.md                  # Deployment instructions
│
├── 📁 Security & Testing
│   ├── test_security.py           # 🆕 Security system testing suite
│   ├── basic-sec-hardening.md     # 🆕 Security implementation documentation
│   └── SECURITY_INCIDENT.md       # 🚫 Security incident report (gitignored)
│
├── 📁 Visual Assets
│   └── assets/
│       ├── bot-profile-512.svg    # Bot profile image (vector)
│       ├── bot-profile-512.png    # Bot profile image (raster)
│       ├── favicon.svg            # Bot favicon
│       ├── index.html             # Asset preview page
│       └── README.md              # Asset documentation
│
└── 📁 Documentation
    └── README.md                  # Main project documentation
```

## Configuration ⚙️

### Environment Variables

- `TELEGRAM_BOT_TOKEN` (required): Your Telegram Bot token
- `DEBUG` (optional): Set to `True` for debug logging

### Scraper Settings

The bot is configured to:
- Fetch data from pump.fun with newest coins first
- Display top coins
- Timeout after 30 seconds for web requests
- Use a realistic User-Agent header

## Development 🛠️

### Extending the Scraper

The scraper in `scraper.py` uses BeautifulSoup to parse the pump.fun website. To improve coin detection:

1. Inspect the actual HTML structure of pump.fun
2. Update the `_parse_coins_from_html` method with proper CSS selectors
3. Test with different site layouts

### Adding Features

Some ideas for enhancements:
- Add coin filtering by market cap or volume
- Implement price alerts
- Add historical data tracking
- Support for other DEX platforms
- Database storage for coin history

### Testing

To test the bot:

1. Create a test bot with BotFather
2. Use the test bot token in development
3. Test all commands and button interactions
4. Verify error handling with invalid inputs

## Troubleshooting 🔧

### Common Issues

**"Configuration error: TELEGRAM_BOT_TOKEN environment variable is required"**
- Make sure your `.env` file exists and contains your bot token
- Verify the token format (should start with a number followed by a colon)

**"Error fetching data from pump.fun"**
- Check your internet connection
- The pump.fun website might be temporarily unavailable
- The site structure may have changed (requires scraper updates)

**Bot doesn't respond to commands**
- Verify the bot is running without errors
- Check that you're messaging the correct bot
- Ensure the bot token is valid

### Debug Mode

Enable debug logging by setting `DEBUG=True` in your `.env` file:

```env
DEBUG=True
```

This will provide detailed logging information to help diagnose issues.

### Logs

The bot logs important events and errors. Monitor the console output for:
- Startup messages
- User interactions
- Scraping status
- Error messages

## Security Considerations 🔒

- Never commit your `.env` file or expose your bot token
- The bot doesn't store user data, but be mindful of privacy
- Consider rate limiting for high-traffic scenarios
- Keep dependencies updated for security patches

## Legal and Disclaimer ⚖️

- This bot is for educational and informational purposes only
- Cryptocurrency investments carry risk - always DYOR (Do Your Own Research)
- The bot scrapes publicly available data from pump.fun
- Respect pump.fun's terms of service and rate limits
- No financial advice is provided by this bot

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is open source. Please check the LICENSE file for details.

## Support 💬

For issues and questions:
1. Check this README for common solutions
2. Review the troubleshooting section
3. Check the console logs for error messages
4. Open an issue with detailed information about your problem

---

**Happy trading! 🚀** Remember to always do your own research before making any investment decisions.
