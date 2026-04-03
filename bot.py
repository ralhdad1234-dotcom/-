from telegram import *
from telegram.ext import *
import config
from database import *
from usdt import *

setup()
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    btn = [[InlineKeyboardButton("تحقق", callback_data="check")]]
    await update.message.reply_text("اشترك في القنوات ثم اضغط تحقق", reply_markup=InlineKeyboardMarkup(btn))

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.message.edit_text("✅ تم الدخول\nاكتب /menu")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("💰 نقاطي", callback_data="points")],
        [InlineKeyboardButton("💳 شحن", callback_data="deposit")],
        [InlineKeyboardButton("👥 إحالة", callback_data="ref")]
    ]
    await update.message.reply_text("اختر:", reply_markup=InlineKeyboardMarkup(kb))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id

    if q.data == "points":
        pts = c.execute("SELECT points FROM users WHERE user_id=?", (uid,)).fetchone()[0]
        await q.message.edit_text(f"💰 نقاطك: {pts}")
    elif q.data == "deposit":
        user_state[uid] = "await_tx"
        await q.message.reply_text(f"💸 أرسل TXID إلى هذا العنوان:\n{config.USDT_ADDRESS}")
    elif q.data == "ref":
        link = f"https://t.me/{config.BOT_USERNAME}?start={uid}"
        await q.message.reply_text(f"🔗 رابط إحالتك:\n{link}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    txt = update.message.text

    if user_state.get(uid) == "await_tx":
        ok, amount = check_usdt(txt)
        if ok:
            points = int(amount * config.POINTS_PER_DOLLAR)
            c.execute("UPDATE users SET points = points + ? WHERE user_id=?", (points, uid))
            conn.commit()
            await update.message.reply_text(f"✅ تم شحن {points} نقطة")
        else:
            await update.message.reply_text("❌ TX غير صحيح")
        user_state[uid] = None

app = ApplicationBuilder().token(config.TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()