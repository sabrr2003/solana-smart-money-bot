import requests
import time
from config import BIRDEYE_API_KEY, TELEGRAM_TOKEN, CHAT_ID

# ====== FILTERS ======
MIN_LIQ = 10000
MAX_LIQ = 999999999
MIN_VOLUME = 1000

# ====== TELEGRAM ======
def send_telegram(token, liquidity, volume, price):
    message = f"""
🚨 *SMART MONEY ALERT* 🚨

🪙 *Token:* `{token}`

💧 *Liquidity:* ${liquidity:,.0f}
📊 *Volume 24h:* ${volume:,.0f}
💰 *Price:* ${price}

🔥 *Status:* Activity Detected

🔗 [View Chart](https://dexscreener.com/solana/{token})

🧠 *Source:* Fast Scanner
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload)
    except:
        print("Telegram Error")

# ====== FETCH TOKENS ======
def get_tokens():
    url = "https://public-api.birdeye.so/defi/tokenlist"

    headers = {
        "X-API-KEY": BIRDEYE_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("data", [])
    except:
        print("API Error")
        return []

# ====== MAIN LOOP ======
def main():
    print("🚀 FAST NEWS BOT STARTED")

    seen = set()

    while True:
        tokens = get_tokens()

        for token in tokens:
            try:
                address = token.get("address")
                liquidity = token.get("liquidity", 0)
                volume = token.get("volume24h", 0)
                price = token.get("price", 0)

                # FILTER
                if (
                    liquidity > MIN_LIQ and
                    liquidity < MAX_LIQ and
                    volume > MIN_VOLUME and
                    address not in seen
                ):
                    print("FOUND:", address)

                    send_telegram(address, liquidity, volume, price)

                    seen.add(address)

            except:
                continue

        time.sleep(10)

# ====== RUN ======
if __name__ == "__main__":
    main()
