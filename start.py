#!/usr/bin/env python3
"""
Startup script for PEAAS Media Downloader Bot
Handles environment setup and bot initialization
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import telegram
        import yt_dlp
        import requests
        import instaloader
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check environment variables"""
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
        print("Please:")
        print("1. Copy .env.example to .env")
        print("2. Add your Telegram bot token to .env")
        print("3. Get token from @BotFather on Telegram")
        return False
    
    print("✅ Environment variables configured")
    return True

def create_directories():
    """Create necessary directories"""
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    print("✅ Downloads directory ready")

def main():
    """Main startup function"""
    print("🤖 Starting PEAAS Media Downloader Bot...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("=" * 50)
    print("🚀 Starting bot...")
    
    # Import and run the bot
    try:
        from bot import main as bot_main
        bot_main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()