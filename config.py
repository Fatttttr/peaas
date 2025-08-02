#!/usr/bin/env python3
"""
Configuration module for PEAAS Media Downloader Bot
"""

import os
from pathlib import Path

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WHATSAPP_BOT_TOKEN = os.getenv('WHATSAPP_BOT_TOKEN')

# Download Configuration
DOWNLOADS_DIR = Path("downloads")
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 100))
DOWNLOAD_TIMEOUT_SECONDS = int(os.getenv('DOWNLOAD_TIMEOUT_SECONDS', 300))

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Platform-specific settings
YOUTUBE_OPTS = {
    'format': 'best[height<=720]',
    'outtmpl': str(DOWNLOADS_DIR / '%(title)s.%(ext)s'),
    'noplaylist': True,
    'max_filesize': MAX_FILE_SIZE_MB * 1024 * 1024,  # Convert MB to bytes
}

SUPPORTED_PLATFORMS = {
    'youtube': ['youtube.com', 'youtu.be'],
    'tiktok': ['tiktok.com', 'vm.tiktok.com'],
    'instagram': ['instagram.com'],
    'spotify': ['spotify.com']
}

# Bot Messages
WELCOME_MESSAGE = """
🤖 **Welcome to PEAAS Media Downloader Bot!**

I can help you download media from various platforms:
• 🎥 YouTube
• 📱 TikTok  
• 📸 Instagram
• 🎵 Spotify (limited)

**Commands:**
/download <platform> <url> - Download media
/help - Show this help message

**Example:**
`/download youtube https://youtube.com/watch?v=...`
`/download tiktok https://vm.tiktok.com/...`
`/download instagram https://instagram.com/p/...`

Just send me a URL and I'll try to detect the platform automatically! 🚀
"""

HELP_MESSAGE = """
📖 **How to use this bot:**

**Method 1: Command**
`/download <platform> <url>`

**Method 2: Direct URL**
Just send me any supported URL directly!

**Supported Platforms:**
• YouTube (youtube, yt)
• TikTok (tiktok, tt)
• Instagram (instagram, ig)
• Spotify (spotify) - Limited support

**Examples:**
• `/download youtube https://youtube.com/watch?v=dQw4w9WgXcQ`
• `/download tiktok https://vm.tiktok.com/ZMd7qJ9qJ/`
• Just send: `https://instagram.com/p/ABC123/`

⚠️ **Note:** Please respect copyright and platform terms of service.
"""