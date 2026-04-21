import requests
import time
from config import *

headers = {"X-API-KEY": API_KEY}

seen = set()
wallets = {}
smart_wallets = set()

# =====================
# Telegram
# =====================
def send(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=3)
    except:
        print(msg)

# =====================
# Trades
# =====================
def get_trades():
    try:
        url = "https://public-api.birdeye.so/public/transactions"
        r = requests.get(url, headers=headers, timeout=3)
        return r.json().get("data", [])
    except:
        return []

# =====================
# Filters
# =====================
def is_meme(name):
    name = name.lower()
    return any(x in name for x in ["dog","inu","pepe","cat","shib","meme"])

def is_scam(name):
    name = name.lower()
    return any(x in name for x in ["test","rug","fake","scam"])

# =====================
# Smart scoring
# =====================
def update_wallet(wallet, amount):
    if wallet not in wallets:
        wallets[wallet] = {"count":0,"volume":0,"score":0}

    w = wallets[wallet]

    w["count"] += 1
    w["volume"] += amount
    w["score"] = w["count"]*2 + w["volume"]/5000

    if w["score"] > 20:
        smart_wallets.add(wallet)

# =====================
# Main loop
# =====================
def run():
    print("🚀 FAST NEWS BOT STARTED")

    while True:
        trades = get_trades()

        for t in trades:
            try:
                wallet = t.get("owner")
                token = t.get("address")
                amount = t.get("valueUsd", 0)
                symbol = t.get("symbol","UNK")

                if not wallet or not token:
                    continue

                if amount < MIN_BUY or amount > MAX_BUY:
                    continue

                if not is_meme(symbol):
                    continue

                if is_scam(symbol):
                    continue

                key = f"{wallet}_{token}"
                if key in seen:
                    continue

                seen.add(key)

                update_wallet(wallet, amount)

                # 🔥 SMART MONEY
                if wallet in smart_wallets:
                    send(f"""
🧠 SMART MONEY

💰 ${amount:,.0f}
🪙 {symbol}

📌 {token}
""")

                # 🐋 WHALE
                elif amount > 20000:
                    send(f"""
🐋 WHALE BUY

💰 ${amount:,.0f}
🪙 {symbol}

📌 {token}
""")

                # 🚀 DEAD PUMP
                elif amount > 80000:
                    send(f"""
🚀 DEAD COIN REVIVE

💰 ${amount:,.0f}
🪙 {symbol}

📌 {token}
""")

            except:
                continue

        time.sleep(1)  # ⚡ سرعة عالية

if __name__ == "__main__":
    run()
