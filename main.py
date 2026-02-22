from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers import start, user_message, admin_reply

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.REPLY, user_message))
    app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, admin_reply))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
