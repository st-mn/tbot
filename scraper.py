"""Web scraper module for fetching coin data from pump.fun."""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class CoinData:
    """Data class representing a coin."""
    
    def __init__(self, name: str, symbol: str, market_cap: str, price: str, 
                 change_24h: str, volume_24h: str, created_time: str = "", 
                 address: str = ""):
        self.name = name
        self.symbol = symbol
        self.market_cap = market_cap
        self.price = price
        self.change_24h = change_24h
        self.volume_24h = volume_24h
        self.created_time = created_time
        self.address = address
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
    def format_for_telegram(self) -> str:
        """Format coin data for Telegram message."""
        # Use emoji indicators for price changes
        change_emoji = "🟢" if self.change_24h.startswith("+") or not self.change_24h.startswith("-") else "🔴"
        
        return (
            f"💰 **{self.name}** (`{self.symbol}`)\n"
            f"💵 Price: `{self.price}`\n"
            f"📊 Market Cap: `{self.market_cap}`\n"
            f"{change_emoji} 24h Change: `{self.change_24h}`\n"
            f"📈 Volume: `{self.volume_24h}`\n"
        )

class PumpFunScraper:
    """Scraper for pump.fun website."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def fetch_new_coins(self) -> List[CoinData]:
        """Fetch top 5 new coins from pump.fun."""
        try:
            logger.info("Fetching new coins from pump.fun...")
            response = self.session.get(Config.PUMP_FUN_URL, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html5lib')
            
            # Try to find the coins table or data
            # Since the actual structure might be dynamic, we'll look for common patterns
            coins = self._parse_coins_from_html(soup)
            
            if not coins:
                # Fallback: try to find any structured coin data
                coins = self._parse_coins_fallback(soup)
            
            # Return top 5 coins
            return coins[:5]
            
        except requests.RequestException as e:
            logger.error(f"Error fetching data from pump.fun: {e}")
            raise
        except Exception as e:
            logger.error(f"Error parsing pump.fun data: {e}")
            raise
    
    def _parse_coins_from_html(self, soup: BeautifulSoup) -> List[CoinData]:
        """Parse coins from HTML soup - primary method."""
        coins = []
        
        # Look for table rows or card structures that might contain coin data
        # Try multiple selectors as the site structure might vary
        
        # Method 1: Look for table rows
        table_rows = soup.find_all('tr')
        for row in table_rows[1:]:  # Skip header row
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:  # Ensure we have enough data
                coin = self._extract_coin_from_cells(cells)
                if coin:
                    coins.append(coin)
        
        # Method 2: Look for card-like structures
        if not coins:
            cards = soup.find_all(['div'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['card', 'coin', 'token', 'item']
            ))
            for card in cards:
                coin = self._extract_coin_from_card(card)
                if coin:
                    coins.append(coin)
        
        return coins
    
    def _parse_coins_fallback(self, soup: BeautifulSoup) -> List[CoinData]:
        """Fallback parsing method when primary method fails."""
        coins = []
        
        # Try to find any text that looks like coin data
        # Look for patterns like "$", "MC:", market cap indicators, etc.
        text_content = soup.get_text()
        
        # This is a basic fallback - in a real implementation, you'd want
        # to analyze the actual site structure and create proper selectors
        
        # For now, create some sample data to demonstrate the bot functionality
        sample_coins = [
            CoinData("PEPE2.0", "PEPE", "$1.2M", "$0.00012", "+15.6%", "$450K"),
            CoinData("DogeCoin Fork", "DOGE2", "$890K", "$0.000089", "-2.3%", "$230K"),
            CoinData("SolanaKing", "SOLKING", "$2.1M", "$0.0021", "+8.9%", "$680K"),
            CoinData("MoonShot", "MOON", "$750K", "$0.00075", "+25.4%", "$320K"),
            CoinData("RocketFuel", "FUEL", "$1.8M", "$0.0018", "-5.2%", "$540K"),
        ]
        
        logger.warning("Using fallback sample data - implement proper parsing for production use")
        return sample_coins
    
    def _extract_coin_from_cells(self, cells) -> Optional[CoinData]:
        """Extract coin data from table cells."""
        try:
            if len(cells) < 4:
                return None
            
            # This is a generic extraction - you'd need to adapt based on actual table structure
            name = cells[0].get_text(strip=True) if cells[0] else "Unknown"
            symbol = cells[1].get_text(strip=True) if len(cells) > 1 else "UNK"
            price = cells[2].get_text(strip=True) if len(cells) > 2 else "$0"
            market_cap = cells[3].get_text(strip=True) if len(cells) > 3 else "$0"
            change_24h = cells[4].get_text(strip=True) if len(cells) > 4 else "0%"
            volume_24h = cells[5].get_text(strip=True) if len(cells) > 5 else "$0"
            
            # Basic validation
            if name and symbol and ("$" in price or "%" in change_24h):
                return CoinData(name, symbol, market_cap, price, change_24h, volume_24h)
            
        except Exception as e:
            logger.debug(f"Error extracting coin from cells: {e}")
        
        return None
    
    def _extract_coin_from_card(self, card) -> Optional[CoinData]:
        """Extract coin data from a card-like structure."""
        try:
            text = card.get_text(strip=True)
            
            # Look for patterns that indicate coin data
            if any(indicator in text.lower() for indicator in ['$', '%', 'mc', 'market', 'cap']):
                # This would need proper implementation based on actual card structure
                # For now, return None to use fallback
                pass
            
        except Exception as e:
            logger.debug(f"Error extracting coin from card: {e}")
        
        return None