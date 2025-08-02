#!/usr/bin/env python3
"""
Multi-Platform Bot with Media Download Capabilities
Supports WhatsApp and Telegram with downloading from YouTube, Spotify, TikTok, Instagram, etc.
"""

import os
import logging
import asyncio
from pathlib import Path
from typing import Optional

# Telegram imports
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Media downloader imports
import yt_dlp
import requests
from pytube import YouTube
import instaloader
from tiktok_downloader import snaptik

# Local imports
from config import (
    TELEGRAM_BOT_TOKEN, WHATSAPP_BOT_TOKEN, DOWNLOADS_DIR,
    YOUTUBE_OPTS, SUPPORTED_PLATFORMS, WELCOME_MESSAGE, HELP_MESSAGE,
    LOG_LEVEL
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

# Create downloads directory
DOWNLOADS_DIR.mkdir(exist_ok=True)


class MediaDownloader:
    """Handles downloading media from various platforms"""
    
    def __init__(self):
        self.yt_opts = YOUTUBE_OPTS
    
    async def download_youtube(self, url: str) -> str:
        """Download YouTube video"""
        try:
            with yt_dlp.YoutubeDL(self.yt_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                
                # Download the video
                ydl.download([url])
                return f"✅ YouTube video downloaded successfully!\n📹 Title: {title}"
        except Exception as e:
            logger.error(f"YouTube download error: {e}")
            return f"❌ Error downloading YouTube video: {str(e)}"

    async def download_tiktok(self, url: str) -> str:
        """Download TikTok video"""
        try:
            # Use snaptik for TikTok downloads
            result = snaptik(url)
            if result:
                video_url = result[0].get('url')
                if video_url:
                    # Download the video
                    response = requests.get(video_url)
                    filename = DOWNLOADS_DIR / f"tiktok_{hash(url)}.mp4"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    return f"✅ TikTok video downloaded successfully!\n📱 Saved as: {filename.name}"
            return "❌ Could not extract TikTok video"
        except Exception as e:
            logger.error(f"TikTok download error: {e}")
            return f"❌ Error downloading TikTok video: {str(e)}"

    async def download_instagram(self, url: str) -> str:
        """Download Instagram content"""
        try:
            L = instaloader.Instaloader(dirname_pattern=str(DOWNLOADS_DIR))
            
            # Extract shortcode from URL
            if '/p/' in url:
                shortcode = url.split('/p/')[1].split('/')[0]
            elif '/reel/' in url:
                shortcode = url.split('/reel/')[1].split('/')[0]
            else:
                return "❌ Invalid Instagram URL format"
            
            # Download post
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target='instagram')
            
            return f"✅ Instagram content downloaded successfully!\n📸 Post by: @{post.owner_username}"
        except Exception as e:
            logger.error(f"Instagram download error: {e}")
            return f"❌ Error downloading Instagram content: {str(e)}"

    async def download_spotify(self, url: str) -> str:
        """Download Spotify track (Note: This is for educational purposes)"""
        try:
            # Note: Spotify downloading requires special handling due to DRM
            # This is a placeholder - actual implementation would need spotify-dl or similar
            return "⚠️ Spotify downloading requires additional setup and may violate ToS.\nPlease use official Spotify app for music streaming."
        except Exception as e:
            logger.error(f"Spotify download error: {e}")
            return f"❌ Error with Spotify download: {str(e)}"


class TelegramBot:
    """Telegram bot handler"""
    
    def __init__(self, token: str):
        self.token = token
        self.downloader = MediaDownloader()
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("download", self.download_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(HELP_MESSAGE, parse_mode='Markdown')
    
    async def download_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /download command"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ Please use format: `/download <platform> <url>`\n"
                "Example: `/download youtube https://youtube.com/watch?v=...`",
                parse_mode='Markdown'
            )
            return
        
        platform = context.args[0].lower()
        url = context.args[1]
        
        await self._process_download(update, platform, url)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle direct URL messages"""
        message_text = update.message.text
        
        # Auto-detect platform from URL
        if 'youtube.com' in message_text or 'youtu.be' in message_text:
            platform = 'youtube'
        elif 'tiktok.com' in message_text or 'vm.tiktok.com' in message_text:
            platform = 'tiktok'
        elif 'instagram.com' in message_text:
            platform = 'instagram'
        elif 'spotify.com' in message_text:
            platform = 'spotify'
        else:
            await update.message.reply_text(
                "🤔 I couldn't detect the platform. Please use:\n"
                "`/download <platform> <url>`\n\n"
                "Or send a direct URL from: YouTube, TikTok, Instagram, or Spotify",
                parse_mode='Markdown'
            )
            return
        
        await self._process_download(update, platform, message_text)
    
    async def _process_download(self, update: Update, platform: str, url: str):
        """Process download request"""
        # Send processing message
        processing_msg = await update.message.reply_text(f"⏳ Processing {platform} download...")
        
        try:
            if platform in ['youtube', 'yt']:
                result = await self.downloader.download_youtube(url)
            elif platform in ['tiktok', 'tt']:
                result = await self.downloader.download_tiktok(url)
            elif platform in ['instagram', 'ig']:
                result = await self.downloader.download_instagram(url)
            elif platform == 'spotify':
                result = await self.downloader.download_spotify(url)
            else:
                result = f"❌ Unsupported platform: {platform}\nSupported: youtube, tiktok, instagram, spotify"
            
            # Edit the processing message with result
            await processing_msg.edit_text(result)
            
        except Exception as e:
            logger.error(f"Download processing error: {e}")
            await processing_msg.edit_text(f"❌ An error occurred: {str(e)}")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")
        self.application.run_polling()


class WhatsAppBot:
    """WhatsApp bot handler (placeholder for future implementation)"""
    
    def __init__(self, token: str):
        self.token = token
        self.downloader = MediaDownloader()
    
    def send_message(self, to: str, message: str):
        """Send WhatsApp message"""
        # Placeholder for WhatsApp API implementation
        logger.info(f"WhatsApp message to {to}: {message}")
        print(f"WhatsApp -> {to}: {message}")
    
    def setup_webhook(self):
        """Setup WhatsApp webhook"""
        # Placeholder for webhook setup
        logger.info("WhatsApp webhook setup (placeholder)")


def main():
    """Main function to run the bot"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set your TELEGRAM_BOT_TOKEN environment variable")
        return
    
    try:
        # Initialize and start Telegram bot
        telegram_bot = TelegramBot(TELEGRAM_BOT_TOKEN)
        
        # Initialize WhatsApp bot (if token provided)
        if WHATSAPP_BOT_TOKEN:
            whatsapp_bot = WhatsAppBot(WHATSAPP_BOT_TOKEN)
            whatsapp_bot.setup_webhook()
            logger.info("WhatsApp bot initialized")
        else:
            logger.warning("WHATSAPP_BOT_TOKEN not provided, WhatsApp functionality disabled")
        
        # Start the Telegram bot
        telegram_bot.run()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()