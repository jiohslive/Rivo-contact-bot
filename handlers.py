import asyncio
from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.error import Forbidden, BadRequest
from telegram.ext import ContextTypes

from config import ADMIN_ID, WELCOME_TEXT
from storage import save_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)

    await update.message.reply_text(
        WELCOME_TEXT.format(name=user.first_name),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    save_user(user.id)

    try:
        await context.bot.send_chat_action(chat_id=ADMIN_ID, action=ChatAction.TYPING)
    except:
        pass

    text = (
        f"👤 <b>{user.first_name}</b>\n"
        f"🆔 {user.id}\n\n"
        f"{msg.text or ''}\n\n"
        f"👉 Reply to this message to answer."
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text,
            parse_mode=ParseMode.HTML
        )
    except BadRequest:
        print("❌ ADMIN_ID wrong or admin has not started the bot.")
    except Forbidden:
        print("❌ Bot blocked by admin.")

    sent = await msg.reply_text("✅ Message sent!")
    await asyncio.sleep(4)
    try:
        await sent.delete()
    except:
        pass

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        return

    replied_text = update.message.reply_to_message.text or ""
    lines = replied_text.splitlines()

    user_id = None
    for line in lines:
        if line.startswith("🆔"):
            user_id = line.replace("🆔", "").strip()
            break

    if not user_id:
        return

    try:
        await context.bot.send_chat_action(chat_id=int(user_id), action=ChatAction.TYPING)
        await context.bot.send_message(
            chat_id=int(user_id),
            text=update.message.text
        )
    except Forbidden:
        await update.message.reply_text("❌ User has blocked the bot.")
        return
    except BadRequest:
        await update.message.reply_text("❌ Failed to send message.")
        return

    status_msg = await update.message.reply_text("Reply Sent ✅")
    await asyncio.sleep(2)
    try:
        await status_msg.delete()
    except:
        pass
