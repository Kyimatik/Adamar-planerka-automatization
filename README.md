# 🤖 Adamar Team Bot

A Telegram bot designed for the **Adamar** team to streamline communication, automate daily planning, and collect anonymous feedback or problems.

## 📌 Features

- 🧠 **Daily Stand-ups**: Team members can submit daily reports saved to Google Sheets
- 💡 **Anonymous Suggestions**: Share improvement ideas anonymously
- 🛠 **Anonymous Issues**: Report team issues or blockers confidentially
- 📬 **Automatic Reminders**: Daily reminders to fill in stand-up reports
- 🛡 **Admin Panel**: Broadcast messages, manage members, and control cron jobs

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/adamar-bot.git
cd adamar-bot
2. Install Dependencies
bash
Копировать
Редактировать
pip install -r requirements.txt
3. Add Environment Variables
Create a .env file in the root directory and add:


BOT_TOKEN=your_telegram_bot_token
GOOGLE_SHEET_ID=your_google_sheet_id
ADMINS=123456789 987654321  # space-separated Telegram user IDs
4. Setup Google Sheets API
Enable the Google Sheets API

Create a service account and download its credentials .json file

Share the Google Sheet with the service account’s email

🧠 Technologies Used
Python 🐍

Aiogram v3

Google Sheets API

JSON Storage

FSM (Finite State Machine)

📎 Bot Commands
Command	Description
/start	Welcome message and help
/planerka	Submit a daily report
/suggest	Send an anonymous suggestion
/problem	Report an anonymous issue
/send	(admin) Broadcast a message

📬 Contact
Developer: y.emirlan08@gmail.com
Created for internal use by the Adamar team.

Author  -  Ysmanov Emirlan
