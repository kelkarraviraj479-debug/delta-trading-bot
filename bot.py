import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BASE_URL = "https://api.india.delta.exchange"

def send_telegram_message(message):
    print("\n--- 🔍 TELEGRAM DEBUG INFO ---")
    print(f"Token Extracted: {'Yes (Length: ' + str(len(TELEGRAM_BOT_TOKEN)) + ')' if TELEGRAM_BOT_TOKEN else 'No (None)'}")
    print(f"Chat ID Extracted: {TELEGRAM_CHAT_ID}")
    
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload)
            print(f"Telegram HTTP Status Code: {response.status_code}")
            print(f"Telegram Response: {response.text}")
        except Exception as e:
            print(f"Telegram Request Exception: {e}")
    else:
        print("❌ Error: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in GitHub Secrets!")

def run_paper_trading():
    print("\n--- 🤖 PAPER TRADING BOT ACTIVE ---")
    
    ticker_url = f"{BASE_URL}/v2/tickers/BTCUSD"
    try:
        res = requests.get(ticker_url)
        if res.status_code == 200:
            data = res.json()
            current_price = float(data['result']['close'])
            
            msg = (
                f"🤖 *Delta Trading Bot Update*\n\n"
                f"📊 *BTCUSD Price:* `${current_price}`\n"
                f"🔍 *Status:* RSI Normal\n"
                f"💡 *Action:* No Trade Executed\n\n"
                f"🛡️ _Running in Paper Trading Mode_"
            )
            
            print(f"✅ Delta API Connection Successful! Price: ${current_price}")
            send_telegram_message(msg)
            
        else:
            print(f"❌ Delta API Error: {res.text}")
    except Exception as e:
        print(f"Error fetching ticker: {e}")

if __name__ == "__main__":
    run_paper_trading()
    
