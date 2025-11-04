# Bot Assets 🎨

This directory contains visual assets for the Pump.fun Telegram Bot.

## Files Included:

### 🚀 **favicon.svg** 
- **Size**: 32x32 pixels
- **Format**: SVG (vector)
- **Use**: Website favicon, GitHub repository icon
- **Design**: Blue background with white rocket, "P" for pump, growth chart line

### 🤖 **bot-profile-512.svg**
- **Size**: 512x512 pixels  
- **Format**: SVG (vector, can be converted to PNG)
- **Use**: Telegram bot profile picture
- **Design**: Detailed rocket with flames, "PUMP" text, growth chart, Telegram bot badge

## 📱 **Using as Telegram Bot Profile Picture:**

1. **Convert to PNG**: Use any SVG to PNG converter to create a 512x512 PNG
   - Online: [svgtopng.com](https://svgtopng.com)
   - Command line: `inkscape bot-profile-512.svg --export-png=bot-profile.png -w 512 -h 512`

2. **Upload to Telegram**:
   - Message [@BotFather](https://t.me/BotFather)
   - Send: `/setuserpic`
   - Select your bot: `@PumpingTbot`
   - Upload the PNG file

## 🌐 **Using as GitHub Repository Icon:**

GitHub will automatically use `favicon.svg` or convert it to favicon.ico for your repository if placed in the root or assets folder.

## 🎨 **Design Elements:**

- **🚀 Rocket**: Represents "pump" and growth
- **📈 Chart Lines**: Shows upward price movement
- **💙 Blue Theme**: Telegram brand colors
- **⭐ Gold Accents**: Premium/valuable coins
- **🤖 Bot Badge**: Clearly indicates it's a Telegram bot

## 🔧 **Customization:**

All files are SVG format, so you can:
- Edit colors in any text editor
- Modify text and elements
- Scale to any size without quality loss
- Convert to PNG, ICO, or other formats as needed

## � **Converting SVG to PNG:**

### Option 1: Automated Script
Run the conversion script from repository root:
```bash
# Windows
convert_assets.bat

# Linux/Mac
python3 convert_assets.py
```

### Option 2: Online Converter
1. Go to [svgtopng.com](https://svgtopng.com)
2. Upload `bot-profile-512.svg`
3. Set size to 512x512 pixels
4. Download PNG
5. Add to repository

### Option 3: Command Line Tools
```bash
# Using Inkscape
inkscape bot-profile-512.svg --export-png=bot-profile-512.png -w 512 -h 512

# Using ImageMagick
convert bot-profile-512.svg -resize 512x512 bot-profile-512.png
```

## �📦 **Additional Sizes:**

If you need other sizes, you can easily create them from the SVG files:
- 16x16 (small favicon)
- 64x64 (larger favicon) 
- 256x256 (app icon)
- 1024x1024 (high-res profile)