# 📁 KoloCloud - Хмарне Сховище для Військових Цілей

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Система забезпечує зберігання, шифрування, обробку та пошук документів (у тому числі фото, OCR, PDF, Word, Excel).
Вбудований AI-помічник, чат, кабінети користувачів. Робота локально, доступ через тунель (наприклад, ngrok).

## 🌟 Основні можливості

✅ **Безпечне зберігання файлів** - завантаження, шифрування та управління документами  
✅ **OCR розпізнавання** - автоматичне витягування тексту з зображень  
✅ **AI-помічник** - інтелектуальна обробка документів та запитів  
✅ **Генерація звітів** - створення військових документів за шаблонами  
✅ **Чат в реальному часі** - командне спілкування через WebSocket  
✅ **Авторизація та ролі** - система користувачів (адмін/звичайний)  
✅ **Логування активності** - аудит всіх операцій в системі  

## 📋 Вимоги

- Python 3.8 або вище
- pip (Python package manager)
- Tesseract OCR (для розпізнавання тексту)
- 2GB+ RAM
- 1GB+ вільного місця на диску

## 🚀 Швидкий старт

### Linux/Mac

\`\`\`bash
# Запустити сервер
./start_server.sh
\`\`\`

### Windows

\`\`\`cmd
# Запустити сервер
start_server.bat
\`\`\`

Сервер запуститься на \`http://localhost:5000\`

### Доступ за замовчуванням

- **URL:** http://localhost:5000
- **Логін:** admin
- **Пароль:** admin123

⚠️ **ВАЖЛИВО:** Змініть пароль адміністратора після першого входу!

## 📁 Структура проєкту

\`\`\`
KoloCloud/
├── backend/                    # Серверна частина
│   ├── app.py                 # Головний Flask-сервер
│   ├── config.py              # Конфігурація
│   ├── database/              # Моделі та БД
│   ├── auth/                  # Авторизація
│   ├── files/                 # Робота з файлами
│   ├── ocr/                   # OCR обробка
│   ├── ai_assistant/          # AI помічник
│   ├── chat/                  # WebSocket чат
│   ├── utils/                 # Утиліти
│   └── requirements.txt       # Залежності Python
│
├── frontend/                   # Клієнтська частина
│   ├── static/                # CSS, JS, іконки
│   └── templates/             # HTML шаблони
│
├── data/                       # Дані системи
│   ├── users/                 # Файли користувачів
│   ├── temp/                  # Тимчасові файли
│   └── logs/                  # Логи системи
│
├── config/                     # Конфігураційні файли
│   ├── .env.example           # Приклад налаштувань
│   └── settings.json          # Глобальні налаштування
│
├── start_server.sh            # Запуск (Linux/Mac)
├── start_server.bat           # Запуск (Windows)
└── README.md                  # Документація
\`\`\`

## 📊 Технології

- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-SocketIO
- **Frontend:** HTML5, TailwindCSS, JavaScript, Socket.IO
- **Database:** SQLite (можна замінити на PostgreSQL/MySQL)
- **OCR:** Tesseract, OpenCV, PIL
- **Security:** bcrypt, cryptography
- **AI:** llama-cpp-python (опційно)

---

🇺🇦 Слава Україні! 🇺🇦
