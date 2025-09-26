# 🤖 Aiogram Fastapi Bot Template

[![Actions status](https://github.com/BushlanovDev/aiogram-fastapi-bot-template/actions/workflows/check.yml/badge.svg)](https://github.com/BushlanovDev/aiogram-fastapi-bot-template/actions) 
[![Python](https://img.shields.io/badge/Python-3.12%2B-brightgreen)](https://www.python.org/downloads/) 
[![Aiogram](https://img.shields.io/badge/aiogram-3.17-brightgreen)](https://pypi.org/project/aiogram/)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

A simple template for creating a telegram bot on webhooks using the **aiogram** and **fastapi**

### 💻 Installation

1. Clone project `git clone https://github.com/BushlanovDev/aiogram-fastapi-bot-template.git`
2. Create a virtual venv `python -m venv venv` and `source venv/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. Copy config template `cp .env.example .env`

### ✍️ Configuration

Edit the .env file  
`APP__DEBUG` `true` or `false`, development mode  
`APP__PORT` Port of application for fastapi (`8080`)  
`APP__URL` The base domain of the application (`https://example.com`)  
`APP__WEBHOOK_PATH` The route to which hooks from telegram will come (`/webhook/tg`)  
`APP__DEFAULT_LANGUAGE` Default response language if the user's language is not received in the hook (`en`)  
`TG_BOT__TOKEN` Telegram bot secret token

### 🚀 Run bot

For local launch you will most likely need the application [ngrok](https://ngrok.com/) or similar. `APP__URL` needs to
be copied from ngrok window to config.  
Run bot `python main.py` or `docker compose up -d`

### 📁 Bot structure

| Folder      | Description                              |
|-------------|------------------------------------------|
| callbacks   | Callback data                            |
| configs     | Configuration files                      |
| handlers    | Handlers, commands, callbacks            |
| i18n        | Localization                             |
| keyboards   | Keyboards reply, inline                  |
| middlewares | Middlewares for localization, throttling |
| services    | Custom libraries                         |
| states      | State objects                            |

## 📄 License

This repository's source code is available under the [MIT License](LICENSE).
