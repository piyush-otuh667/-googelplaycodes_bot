# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import random

TOKEN = ("7996827576:AAH-67CWprWUfZHyruEVJiVZr8Z4vXNrT_k")

# --- Generate Random Code ---
def generate_code():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choices(chars, k=16))

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ I Subscribed", callback_data="subscribed")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome to Redeem Master Bot!\n\n"
        "🎯 Pehle mera YouTube channel subscribe karo ❤️\n"
        "👉 [Teach With Piyush](https://youtube.com/@teachwithpiyush?si=jV16crytzwSpLHoo)\n\n"
        "Phir neeche button dabao 👇",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# --- Handle Button Clicks ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Initialize user counter
    if "counter" not in context.user_data:
        context.user_data["counter"] = 0

    # Breakdown check
    if context.user_data["counter"] >= 5:
        await query.edit_message_text("⚠️ Bot breakdown ho gaya bhai 😵\n⏳ 10 min baad try karo phir se.")
        return

    if query.data == "subscribed":
        keyboard = [
            [InlineKeyboardButton("💸 ₹50", callback_data="tier_50"),
             InlineKeyboardButton("💰 ₹100", callback_data="tier_100")],
            [InlineKeyboardButton("🤑 ₹200", callback_data="tier_200"),
             InlineKeyboardButton("💎 ₹350", callback_data="tier_350")],
            [InlineKeyboardButton("👑 ₹500", callback_data="tier_500")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("✅ Shukriya subscribe karne ke liye!\nAb redeem tier choose karo 👇", reply_markup=reply_markup)

    elif query.data.startswith("tier_"):
        tier = query.data.split("_")[1]
        code = generate_code()
        context.user_data["last_tier"] = tier
        context.user_data["counter"] += 1

        keyboard = [[InlineKeyboardButton("🔁 Next Code", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🎁 Your ₹{tier} Redeem Code:\n`{code}`",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "next":
        tier = context.user_data.get("last_tier", "50")
        code = generate_code()
        context.user_data["counter"] += 1

        if context.user_data["counter"] > 5:
            await query.edit_message_text("⚠️ Bot breakdown ho gaya bhai 😵\n⏳ 10 min baad try karo phir se.")
            return

        keyboard = [[InlineKeyboardButton("🔁 Next Code", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🎁 Another ₹{tier} Redeem Code:\n`{code}`",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# --- Main Function ---
def main():
    app = Application.builder().token(TOKEN).concurrent_updates(True).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Redeem Master Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
