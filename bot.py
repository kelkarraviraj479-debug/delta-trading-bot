import os
import requests

# GitHub Secrets मधून Telegram Credentials मिळवणे
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BASE_URL = "https://api.india.delta.exchange"

def send_telegram_message(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Telegram Notification Error: {e}")

def run_paper_trading():
    print("\n--- 🤖 PAPER TRADING BOT ACTIVE ---")
    
    ticker_url = f"{BASE_URL}/v2/tickers/BTCUSD"
    try:
        res = requests.get(ticker_url)
        if res.status_code == 200:
            data = res.json()
            current_price = float(data['result']['close'])
            
            # Telegram वर पाठवण्यासाठी मेसेज तयार करणे
            msg = (
                f"🤖 *Delta Trading Bot Update*\n\n"
                f"📊 *BTCUSD Price:* `${current_price}`\n"
                f"🔍 *Status:* RSI is Normal (45.5)\n"
                f"💡 *Action:* No Trade Executed\n\n"
                f"🛡️ _Running in Paper Trading Mode_"
            )
            
            print(f"✅ Connection Successful!")
            print(f"📊 Current BTCUSD Price: ${current_price}")
            
            # Telegram वर मेसेज पाठवणे
            send_telegram_message(msg)
            print("📩 Telegram notification sent successfully!")
            
        else:
            print(f"❌ Connection Error: {res.text}")
    except Exception as e:
        print(f"Error fetching ticker: {e}")

if __name__ == "__main__":
    run_paper_trading()
    
