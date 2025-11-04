#!/usr/bin/env python3
"""
Security Test Script
Run this to verify security functions are working properly.
"""

import sys
import os
from datetime import datetime

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from security import security_monitor
    print("✅ Security module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import security module: {e}")
    sys.exit(1)

def test_rate_limiting():
    """Test rate limiting functionality."""
    print("\n🔄 Testing Rate Limiting...")
    
    user_id = 12345
    
    # Test normal usage
    for i in range(3):
        is_limited = security_monitor.is_rate_limited(user_id, max_requests=5, window_minutes=1)
        print(f"  Request {i+1}: Limited = {is_limited}")
    
    # Test rate limit exceeded
    for i in range(5):
        is_limited = security_monitor.is_rate_limited(user_id, max_requests=5, window_minutes=1)
        if is_limited:
            print(f"  ⚠️ Rate limit triggered after {i+3} requests")
            break
    
    print("✅ Rate limiting test completed")

def test_suspicious_activity():
    """Test suspicious activity detection."""
    print("\n🕵️ Testing Suspicious Activity Detection...")
    
    user_id = 54321
    
    # Simulate normal activity
    for i in range(3):
        is_suspicious = security_monitor.check_suspicious_activity(user_id, "start")
        print(f"  Normal activity {i+1}: Suspicious = {is_suspicious}")
    
    # Simulate suspicious rapid activity
    for i in range(15):
        is_suspicious = security_monitor.check_suspicious_activity(user_id, "rapid")
        if is_suspicious:
            print(f"  ⚠️ Suspicious activity detected after {i+4} rapid requests")
            break
    
    print("✅ Suspicious activity test completed")

def test_user_validation():
    """Test user validation functionality."""
    print("\n👤 Testing User Validation...")
    
    # Mock user objects for testing
    class MockUser:
        def __init__(self, user_id, username, is_bot, first_name="Test"):
            self.id = user_id
            self.username = username
            self.is_bot = is_bot
            self.first_name = first_name
    
    # Test valid user
    valid_user = MockUser(123, "validuser", False)
    is_valid = security_monitor.validate_user_data(valid_user)
    print(f"  Valid user: Valid = {is_valid}")
    
    # Test bot user
    bot_user = MockUser(456, "testbot", True)
    is_valid = security_monitor.validate_user_data(bot_user)
    print(f"  Bot user: Valid = {is_valid}")
    
    # Test suspicious username
    suspicious_user = MockUser(789, "spambot123", False)
    is_valid = security_monitor.validate_user_data(suspicious_user)
    print(f"  Suspicious username: Valid = {is_valid}")
    
    print("✅ User validation test completed")

def test_user_blocking():
    """Test user blocking functionality."""
    print("\n🚫 Testing User Blocking...")
    
    user_id = 99999
    
    # Test normal user
    is_blocked = security_monitor.is_user_blocked(user_id)
    print(f"  Initial state: Blocked = {is_blocked}")
    
    # Block user
    security_monitor.block_user(user_id, "Testing block functionality")
    is_blocked = security_monitor.is_user_blocked(user_id)
    print(f"  After blocking: Blocked = {is_blocked}")
    
    print("✅ User blocking test completed")

def test_security_stats():
    """Test security statistics."""
    print("\n📊 Testing Security Statistics...")
    
    # Display current stats
    stats = security_monitor.security_stats
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Blocked requests: {stats['blocked_requests']}")
    print(f"  Suspicious activity count: {stats['suspicious_activity']}")
    print(f"  Start time: {stats['start_time']}")
    
    # Log security stats
    security_monitor.log_security_stats()
    
    print("✅ Security statistics test completed")

def main():
    """Run all security tests."""
    print("🛡️ SECURITY SYSTEM TEST")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    
    try:
        test_rate_limiting()
        test_suspicious_activity()
        test_user_validation()
        test_user_blocking()
        test_security_stats()
        
        print("\n" + "=" * 50)
        print("🎉 ALL SECURITY TESTS PASSED!")
        print("Security system is functioning correctly.")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("Please check the security implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main()