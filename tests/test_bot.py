#!/usr/bin/env python3
"""
Simple test script for PEAAS Media Downloader Bot
"""

import asyncio
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import telegram
        import yt_dlp
        import requests
        import instaloader
        from tiktok_downloader import snaptik
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from config import (
            TELEGRAM_BOT_TOKEN, DOWNLOADS_DIR, YOUTUBE_OPTS,
            SUPPORTED_PLATFORMS, WELCOME_MESSAGE, HELP_MESSAGE
        )
        print("✅ Configuration loaded successfully")
        return True
    except ImportError as e:
        print(f"❌ Config error: {e}")
        return False

def test_bot_classes():
    """Test bot class instantiation"""
    try:
        from bot import MediaDownloader, TelegramBot, WhatsAppBot
        
        # Test MediaDownloader
        downloader = MediaDownloader()
        print("✅ MediaDownloader instantiated")
        
        # Test bot classes (without tokens)
        print("✅ Bot classes imported successfully")
        return True
    except Exception as e:
        print(f"❌ Bot class error: {e}")
        return False

def test_directories():
    """Test directory creation"""
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    
    if downloads_dir.exists():
        print("✅ Downloads directory created")
        return True
    else:
        print("❌ Failed to create downloads directory")
        return False

async def test_async_functions():
    """Test async functionality"""
    try:
        from bot import MediaDownloader
        downloader = MediaDownloader()
        
        # Test that async methods exist
        assert hasattr(downloader, 'download_youtube')
        assert hasattr(downloader, 'download_tiktok')
        assert hasattr(downloader, 'download_instagram')
        assert hasattr(downloader, 'download_spotify')
        
        print("✅ Async methods available")
        return True
    except Exception as e:
        print(f"❌ Async test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running PEAAS Bot Tests...")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Config Test", test_config),
        ("Bot Classes Test", test_bot_classes),
        ("Directory Test", test_directories),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
    
    # Run async test
    print(f"\n🔍 Async Test:")
    if asyncio.run(test_async_functions()):
        passed += 1
    total += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to run.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())