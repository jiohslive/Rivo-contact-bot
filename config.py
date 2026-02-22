import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

WELCOME_TEXT = (
    "👋 Hello {name} and welcome to the Bot!\n\n"
    "🧑🏻‍💻 Created By <a href='https://t.me/RivoBots'>RivoBots</a>\n\n"
    "⬇️ <u>Write a message here</u> and you’ll receive a reply as soon as possible."
)
