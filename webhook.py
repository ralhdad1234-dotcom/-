from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- بيانات البوت ---
TOKEN = "8657547531:AAF5Wd2PT9NYGORAg4I3ONGKLWaD97pAv6M"
BOT_USERNAME = "dgnsgjsfbot"
ADMIN_ID = 7897070744
FORCE_CHANNELS = ["@raft_24"]
USDT_ADDRESS = "TBPW3r1i7wrfdfDUicowF8tYRQ8qHoqYXU"
POINTS_PER_DOLLAR = 1000

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- التحقق من الاشتراك ---
def check_subscription(user_id):
    for channel in FORCE_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Error checking {channel}: {e}")
            return False
    return True

# --- استقبال الويب هوك ---
@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def home():
    return 'Bot is alive!', 200

# --- أمر /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        markup = InlineKeyboardMarkup()
        for ch in FORCE_CHANNELS:
            btn = InlineKeyboardButton("اشترك بالقناة", url=f"https://t.me/{ch[1:]}")
            markup.add(btn)
        markup.add(InlineKeyboardButton("تحققت من الاشتراك ✅", callback_data="check_sub"))
        bot.send_message(user_id, "عشان تستخدم البوت لازم تشترك أول:", reply_markup=markup)
    else:
        bot.send_message(
            user_id,
            f"أهلاً {message.from_user.first_name}!\n\n"
            f"عنوان محفظة USDT (TRC20):\n`{USDT_ADDRESS}`\n\n"
            f"كل 1$ = {POINTS_PER_DOLLAR} نقطة.",
            parse_mode="Markdown"
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "تم التحقق بنجاح!")
        bot.send_message(call.from_user.id, "تمام! تقدر تستخدم البوت الآن. أرسل /start")
    else:
        bot.answer_callback_query(call.id, "لسه ما اشتركت!", show_alert=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
