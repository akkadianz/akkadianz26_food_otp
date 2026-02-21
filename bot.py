from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sqlite3
import random
import re

TOKEN = "8438365476:AAEv0q8nqIq-vZIBwfYo4LEaxTtQLa25GoE"

ADMIN_IDS = [6797155121, 6501059047]

conn = sqlite3.connect("food.db", check_same_thread=False)
c = conn.cursor()

def generate_otp():
    return f"{random.randint(0, 9999):04d}"

# =========================
# REGISTER
# =========================

def register(update, context):
    if len(context.args) != 1:
        update.message.reply_text("❗ Use: /register STUDENT_ID")
        return

    reg_id = context.args[0].strip().upper()

    if not re.fullmatch(r"[A-Z0-9]{4,15}", reg_id):
        update.message.reply_text("❗ Invalid Student ID format")
        return

    c.execute("SELECT otp FROM users WHERE reg_id=?", (reg_id,))
    row = c.fetchone()

    if not row:
        update.message.reply_text("❌ Student ID not found.")
        return

    if row[0] is not None:
        update.message.reply_text("❌ OTP already issued for this ID.")
        return

    otp = generate_otp()
    tg_id = update.effective_user.id

    c.execute(
        "UPDATE users SET tg_id=?, otp=? WHERE reg_id=?",
        (tg_id, otp, reg_id)
    )
    conn.commit()

    update.message.reply_text(
        f"✅ Registration successful!\n\n"
        f"🎓 Student ID: {reg_id}\n\n"
        f"🍽 Food OTP: {otp}\n\n"
        "📌 Show this OTP at the food counter."
    )

# =========================
# REDEEM LOGIC
# =========================

def redeem_otp(update, otp):
    if update.effective_user.id not in ADMIN_IDS:
        update.message.reply_text("🚫 UNAUTHORIZED")
        return

    c.execute(
        "SELECT reg_id, redeemed FROM users WHERE otp=?",
        (otp,)
    )
    row = c.fetchone()

    if not row:
        update.message.reply_text("❌ INVALID OTP")
        return

    reg_id, redeemed = row

    if redeemed == 1:
        update.message.reply_text("🔴 USED – DO NOT SERVE")
        return

    c.execute(
        "UPDATE users SET redeemed=1 WHERE otp=?",
        (otp,)
    )
    conn.commit()

    update.message.reply_text(
        f"🟢 VALID – SERVE FOOD\n🎓 Reg ID: {reg_id}"
    )

# =========================
# FAST OTP ENTRY
# =========================

def otp_message(update, context):
    text = update.message.text.strip()
    if re.fullmatch(r"\d{4}", text):
        redeem_otp(update, text)

def redeem_command(update, context):
    if len(context.args) == 1:
        redeem_otp(update, context.args[0])

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("register", register))
dp.add_handler(CommandHandler("redeem", redeem_command))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, otp_message))

updater.start_polling()
print("🤖 One-day symposium bot running...")
updater.idle()