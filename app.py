import os
import threading
from flask import Flask
from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update

# --- تنظیمات ---
TOKEN = os.environ.get("CICFEJ0LBQRXXRXEPKTNWBEJQLZLOTLHQLXKBGRATOPULDQUWPNVUUVXDJIRFRTP")
ADMIN_ID = "u0IfZBu038d45fd15be1dcc778d77abf"
CHANNEL_ID = "testtabligat"

app = Flask(__name__)

# وب سرور ساده برای Render
@app.route('/')
def health():
    return "Bot is running!"

# --- منطق ربات ---
bot = BotClient(TOKEN)
pending_posts = {}

@bot.on_update(filters.text, filters.private)
async def handle_message(client, update: Update):
    user_id = str(update.sender_id)
    text = update.new_message.text

    if user_id == ADMIN_ID:
        if text == "تایید" and ADMIN_ID in pending_posts:
            post_data = pending_posts[ADMIN_ID]
            await client.send_message(CHANNEL_ID, post_data['text'])
            await update.reply("✅ پست توی کانال منتشر شد.")
            del pending_posts[ADMIN_ID]
        elif text == "رد" and ADMIN_ID in pending_posts:
            await update.reply("❌ پست رد شد.")
            del pending_posts[ADMIN_ID]
        else:
            await update.reply("دستور نامعتبر. (تایید/رد)")
        return

    pending_posts[ADMIN_ID] = {'text': text, 'user': user_id}
    admin_msg = f"📩 پست جدید از {user_id}:\n\n{text}\n\nبرای تایید بنویس: تایید\nبرای رد بنویس: رد"
    await client.send_message(ADMIN_ID, admin_msg)
    await update.reply("پستت رفت برای بررسی ✅")

def run_bot():
    bot.run()

if __name__ == "__main__":
    # ربات رو توی یه ترد جدا اجرا کن
    threading.Thread(target=run_bot, daemon=True).start()
    # وب سرور رو برای Render بالا بیار
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)