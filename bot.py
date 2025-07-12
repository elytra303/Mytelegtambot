from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# Вставь свой токен бота
TOKEN = '7787447891:AAGfAjuILNV-Pkys7D37rTiOsHwjHbfeKWE'

# Вставь свой Telegram user ID (узнай у @userinfobot)
ADMIN_ID = 7534482541  # Заменить на свой ID

# Список активных пользователей
active_users = set()

# /start
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
        "20 минут — 5$ (без холда)"
    )
    await update.message.reply_text(message)

# /whatsapp
async def whatsapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📲 Отправить номер", callback_data="send_number")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "✍️ Нажмите кнопку ниже, чтобы начать сдачу WhatsApp:",
        reply_markup=reply_markup
    )

    # Уведомим админа
    user = update.effective_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔔 Пользователь @{user.username or 'Без username'} (ID: {user.id}) нажал /whatsapp"
    )

# Обработка кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    active_users.add(user_id)

    await query.edit_message_text("✍️ Пожалуйста, введите номер или всю информацию для сдачи WhatsApp.\n\nНапишите `/cancel`, чтобы закончить.")

# Обработка сообщений от активных пользователей
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id in active_users:
        username = user.username or "Без username"
        text = update.message.text

        forward_text = (
            f"📩 Новое сообщение от @{username} (ID: {user_id}):\n\n{text}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)

# /cancel — отключает пересылку
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in active_users:
        active_users.remove(user_id)
        await update.message.reply_text("🚫 Режим передачи информации выключен. Чтобы начать заново, напишите /whatsapp.")
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"❌ Пользователь {update.effective_user.username} закончил отправку.")
    else:
        await update.message.reply_text("ℹ️ Вы не активировали режим передачи. Напишите /whatsapp.")

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("whatsapp", whatsapp))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    app.run_polling()

if __name__ == '__main__':
    main()