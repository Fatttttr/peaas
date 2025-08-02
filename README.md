# PEAAS - Multi-Platform Media Downloader Bot

A powerful Telegram and WhatsApp bot that can download media from various platforms including YouTube, TikTok, Instagram, and more.

## 🚀 Features

- **Multi-Platform Support**: Download from YouTube, TikTok, Instagram, Spotify (limited)
- **Telegram Integration**: Full-featured Telegram bot with command support
- **WhatsApp Ready**: Framework ready for WhatsApp integration
- **Auto-Detection**: Automatically detects platform from URLs
- **User-Friendly**: Simple commands and direct URL support
- **Async Processing**: Non-blocking downloads for better performance

## 📋 Supported Platforms

| Platform | Status | Formats |
|----------|--------|---------|
| YouTube | ✅ Full Support | MP4, WebM |
| TikTok | ✅ Full Support | MP4 |
| Instagram | ✅ Full Support | JPG, MP4 |
| Spotify | ⚠️ Limited | Educational purposes only |

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Telegram Bot Token (from @BotFather)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Fatttttr/peaas.git
   cd peaas
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your bot tokens
   ```

4. **Get your Telegram Bot Token**
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Copy the token to your `.env` file

5. **Run the bot**
   ```bash
   python bot.py
   ```

## 🎯 Usage

### Telegram Commands

- `/start` - Welcome message and instructions
- `/help` - Show help and usage examples
- `/download <platform> <url>` - Download media from specified platform

### Examples

```
/download youtube https://youtube.com/watch?v=dQw4w9WgXcQ
/download tiktok https://vm.tiktok.com/ZMd7qJ9qJ/
/download instagram https://instagram.com/p/ABC123/
```

### Direct URL Support

Simply send any supported URL directly to the bot:
```
https://youtube.com/watch?v=dQw4w9WgXcQ
https://vm.tiktok.com/ZMd7qJ9qJ/
https://instagram.com/p/ABC123/
```

## 📁 Project Structure

```
peaas/
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
├── downloads/         # Downloaded media storage
└── README.md          # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Yes |
| `WHATSAPP_BOT_TOKEN` | Your WhatsApp bot token | No |
| `MAX_FILE_SIZE_MB` | Maximum file size limit | No |
| `DOWNLOAD_TIMEOUT_SECONDS` | Download timeout | No |

### Bot Settings

You can modify download settings in the `MediaDownloader` class:

```python
self.yt_opts = {
    'format': 'best[height<=720]',  # Video quality
    'outtmpl': str(DOWNLOADS_DIR / '%(title)s.%(ext)s'),
    'noplaylist': True,
}
```

## 🔧 Development

### Adding New Platforms

1. Create a new method in `MediaDownloader` class
2. Add platform detection in `handle_message` method
3. Add platform handling in `_process_download` method

### WhatsApp Integration

The bot includes a WhatsApp framework. To enable:

1. Uncomment WhatsApp dependencies in `requirements.txt`
2. Get WhatsApp Business API credentials
3. Implement webhook handling in `WhatsAppBot` class

## 📝 Legal Notice

- **Respect Copyright**: Only download content you have rights to
- **Platform Terms**: Comply with each platform's terms of service
- **Educational Use**: This bot is for educational and personal use only
- **No Warranty**: Use at your own risk

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/Fatttttr/peaas/issues) page
2. Create a new issue with detailed information
3. Include error logs and steps to reproduce

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [instaloader](https://github.com/instaloader/instaloader) - Instagram downloader
- [tiktok-downloader](https://github.com/JuanBindez/tiktok-downloader) - TikTok downloader

---

**⭐ Star this repository if you find it useful!**
