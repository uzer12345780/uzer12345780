# 🚀 KoloCloud Quick Start Guide

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- pip (Python package installer)
- Internet connection (for initial setup)

## Quick Installation

### Option 1: Automatic Setup (Recommended)

**Linux/Mac:**
```bash
./start_server.sh
```

**Windows:**
```cmd
start_server.bat
```

The script will automatically:
1. Create a virtual environment
2. Install all dependencies
3. Create necessary directories
4. Start the server

### Option 2: Manual Setup

1. **Create virtual environment:**
```bash
python3 -m venv venv
```

2. **Activate virtual environment:**

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r backend/requirements.txt
```

4. **Start the server:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
python backend/app.py
```

## First Login

1. Open your browser and navigate to: **http://localhost:5000**

2. Use the default credentials:
   - **Username:** `admin`
   - **Password:** `admin123`

3. **IMPORTANT:** Change the admin password immediately after first login!

## Basic Features

### 1. File Upload
- Go to **Files** section
- Click **Upload File**
- Select file, add tags (optional), enable encryption (optional)
- Click **Upload**

### 2. OCR Text Recognition
- Go to **OCR** section
- Select an image file
- Choose language (Ukrainian + English by default)
- Click **Recognize Text**
- Text will be displayed and can be copied or downloaded

### 3. AI Assistant
- Go to **AI Assistant** section
- Type your question in the chat
- AI will respond (requires LLM model - optional)
- Use quick actions for templates and summaries

### 4. Real-time Chat
- Go to **Chat** section
- Select a room (general, command, support)
- Send messages to other users
- See who's online

### 5. Admin Panel (Admin users only)
- Go to **Admin** section
- View system statistics
- Manage users
- View activity logs
- Configure system settings

## Configuration

### Basic Configuration

Create a `.env` file from the example:
```bash
cp config/.env.example config/.env
```

Edit `config/.env` to set:
- `SECRET_KEY` - Random string for session security
- `ENCRYPTION_KEY` - 32-character key for file encryption
- `DATABASE_URI` - Database connection string

### Optional: OCR Setup

Install Tesseract for OCR functionality:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-ukr tesseract-ocr-eng
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

**macOS:**
```bash
brew install tesseract tesseract-lang
```

### Optional: AI Model Setup

To use the AI assistant:
1. Download a GGUF format LLaMA model
2. Place it in a `models/` directory
3. Set `LLM_MODEL_PATH` in `.env` to point to the model

## Accessing from Other Devices

### Using ngrok (Internet Access)

1. Install ngrok: https://ngrok.com/download

2. Start ngrok:
```bash
ngrok http 5000
```

3. Use the provided URL (e.g., `https://xxxx.ngrok.io`)

### Local Network Access

1. Find your local IP address:
```bash
# Linux/Mac
ifconfig | grep "inet "

# Windows
ipconfig
```

2. Access from other devices: `http://YOUR_IP:5000`

## Troubleshooting

### Server won't start
- Check if port 5000 is already in use
- Ensure all dependencies are installed: `pip list`
- Check logs in `data/logs/kolocloud.log`

### Can't login
- Verify database was created: `ls data/kolocloud.db`
- Try default credentials: admin/admin123
- Check browser console for errors

### Files won't upload
- Check `data/users/` directory permissions
- Verify file size is under 100MB
- Check allowed file extensions in config

### OCR not working
- Install Tesseract OCR
- Set `TESSERACT_CMD` in `.env` to correct path
- Install Ukrainian language pack

### Chat not working
- Check if SocketIO is connecting (browser console)
- Ensure port 5000 allows WebSocket connections
- Try refreshing the page

## Security Best Practices

For production use:

1. **Change default passwords immediately**
2. **Set strong SECRET_KEY and ENCRYPTION_KEY**
3. **Use HTTPS (SSL/TLS)**
4. **Set up firewall rules**
5. **Regular database backups**
6. **Use PostgreSQL instead of SQLite**
7. **Enable logging and monitoring**
8. **Restrict file upload types**
9. **Set appropriate file size limits**
10. **Regular security updates**

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Explore the API documentation
- Customize templates and styling
- Set up automated backups
- Configure additional security measures

## Support

For issues or questions:
- Check the [README.md](README.md)
- Create an issue on GitHub
- Review logs in `data/logs/`

---

🇺🇦 **Happy cloud storing!** 🇺🇦
