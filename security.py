"""Security monitoring and protection for Telegram bot."""

import logging
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Set

logger = logging.getLogger(__name__)

class BotSecurityMonitor:
    """Security monitoring and rate limiting for the bot."""
    
    def __init__(self):
        # Rate limiting: user_id -> deque of timestamps
        self.user_requests = defaultdict(lambda: deque(maxlen=10))
        
        # Suspicious activity tracking
        self.suspicious_users = set()
        self.blocked_users = set()
        
        # Request patterns
        self.request_patterns = defaultdict(list)
        
        # Security stats
        self.security_stats = {
            'total_requests': 0,
            'blocked_requests': 0,
            'suspicious_activity': 0,
            'start_time': datetime.now()
        }
    
    def is_rate_limited(self, user_id: int, max_requests: int = 5, window_minutes: int = 1) -> bool:
        """Check if user is rate limited."""
        now = time.time()
        window_start = now - (window_minutes * 60)
        
        # Clean old requests
        user_deque = self.user_requests[user_id]
        while user_deque and user_deque[0] < window_start:
            user_deque.popleft()
        
        # Check rate limit
        if len(user_deque) >= max_requests:
            logger.warning(f"Rate limit exceeded for user {user_id}: {len(user_deque)} requests in {window_minutes}m")
            return True
        
        # Add current request
        user_deque.append(now)
        return False
    
    def check_suspicious_activity(self, user_id: int, command: str) -> bool:
        """Check for suspicious activity patterns."""
        now = datetime.now()
        
        # Record the pattern
        self.request_patterns[user_id].append((command, now))
        
        # Clean old patterns (keep last hour)
        cutoff = now - timedelta(hours=1)
        self.request_patterns[user_id] = [
            (cmd, ts) for cmd, ts in self.request_patterns[user_id] if ts > cutoff
        ]
        
        patterns = self.request_patterns[user_id]
        
        # Check for spam patterns
        if len(patterns) > 20:  # More than 20 commands in an hour
            self.suspicious_users.add(user_id)
            logger.warning(f"User {user_id} marked as suspicious: {len(patterns)} commands in 1 hour")
            return True
        
        # Check for rapid repetition
        recent = [cmd for cmd, ts in patterns if ts > now - timedelta(minutes=5)]
        if len(recent) > 10:  # More than 10 commands in 5 minutes
            self.suspicious_users.add(user_id)
            logger.warning(f"User {user_id} marked as suspicious: rapid commands")
            return True
        
        return False
    
    def is_user_blocked(self, user_id: int) -> bool:
        """Check if user is blocked."""
        return user_id in self.blocked_users
    
    def block_user(self, user_id: int, reason: str):
        """Block a user."""
        self.blocked_users.add(user_id)
        self.security_stats['blocked_requests'] += 1
        logger.error(f"BLOCKED USER {user_id}: {reason}")
    
    def validate_user_data(self, user) -> bool:
        """Validate user data for suspicious patterns."""
        if not user:
            return False
        
        # Check for bot users (potential automation)
        if user.is_bot:
            logger.warning(f"Bot user detected: {user.id}")
            return False
        
        # Check for users with suspicious usernames
        if user.username:
            suspicious_patterns = ['bot', 'spam', 'scam', 'hack', 'premium', 'gift']
            username_lower = user.username.lower()
            if any(pattern in username_lower for pattern in suspicious_patterns):
                logger.warning(f"Suspicious username pattern: {user.username}")
                return False
        
        return True
    
    def log_security_stats(self):
        """Log current security statistics."""
        uptime = datetime.now() - self.security_stats['start_time']
        
        logger.info("=== SECURITY STATS ===")
        logger.info(f"Uptime: {uptime}")
        logger.info(f"Total requests: {self.security_stats['total_requests']}")
        logger.info(f"Blocked requests: {self.security_stats['blocked_requests']}")
        logger.info(f"Suspicious users: {len(self.suspicious_users)}")
        logger.info(f"Blocked users: {len(self.blocked_users)}")
        logger.info("=====================")

# Global security monitor instance
security_monitor = BotSecurityMonitor()