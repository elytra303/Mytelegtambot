from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = '7787447891:AAGfAjuILNV-Pkys7D37rTiOsHwjHbfeKWE'  # ← Вставь свой токен
ADMIN_ID = 7534482541          # ← Вставь свой Telegram user ID

active_users = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👋 Привет! Добро пожаловать в бот по сдаче WhatsApp!\n\n"
        "📋 Тарифы:\n"
        "1 час — 7$\n"
        "2 часа — 14$\n"
        "3 часа — 24$\n"
        "4 часа — 36$\n"
        "5 часов — 48$\n"
        "6 часов — 54$\n"
        "7 часов — 66$\n"
        "8 часов — 73$\n"
        "9 часов — 79$\n"
        "10 часов — 90$\n"
        "1 минута — 0.1$\n"
        "20 минут — 5$ (без холд)"
    )

    keyboard = [
        [InlineKeyboardButton("📲 Сдача WhatsApp", callback_data="whatsapp")],
        [InlineKeyboardButton("ℹ️ Информация", callback_data="info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup)

# Обработка кнопок /start
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    await query.answer()

    if data == "whatsapp":
        active_users.add(user.id)
        await query.edit_message_text("✍️ Пожалуйста, введите номер для сдачи WhatsApp.\n\nНапишите `/cancel`, чтобы закончить.")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 Пользователь @{user.username or 'Без username'} (ID: {user.id}) нажал Сдача WhatsApp"
        )

    elif data == "info":
        info_text = (
            "ℹ️ Мы берём Ваш WhatsApp для рекламы!\n"
            "💼 Вы предоставляете номер, а мы используем его в рекламных целях.\n"
            "💰 За это Вы получаете оплату по тарифу — всё прозрачно и просто!\n"
            "❗️Если остались вопросы — напишите нам!"
        )
        await query.edit_message_text(info_text)

# Обработка сообщений от активных
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in active_users:
        text = update.message.text
        username = user.username or "Без username"
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Сообщение от @{username} (ID: {user.id}):\n{text}"
        )

# Команда /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id in active_users:
        active_users.remove(user.id)
        await update.message.reply_text("🚫 Режим сдачи WhatsApp завершён.")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"❌ Пользователь @{user.username or 'Без username'} завершил передачу номера."
        )
    else:
        await update.message.reply_text("ℹ️ Вы не активировали режим передачи.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    app.run_polling()

if __name__ == '__main__':
    main()
