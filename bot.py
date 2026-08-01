import os
import requests
import json

# GitHub Secrets मधून API Keys मिळवणे
API_KEY = os.environ.get("DELTA_API_KEY")
API_SECRET = os.environ.get("DELTA_API_SECRET")

BASE_URL = "https://api.india.delta.exchange"

def check_connection():
    if not API_KEY or not API_SECRET:
        print("Error: API_KEY किंवा API_SECRET सापडले नाही! GitHub Secrets तपासा.")
        return False
    
    url = f"{BASE_URL}/v2/wallet/balances"
    headers = {
        "api-key": API_KEY,
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Successfully Connected to Delta Exchange India!")
            return True
        else:
            print(f"❌ Connection Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def run_paper_trading():
    print("\n--- 🤖 PAPER TRADING BOT ACTIVE (DEMO MODE) ---")
    
    # BTCUSD चा थेट लाईव्ह रेट मिळवणे
    ticker_url = f"{BASE_URL}/v2/tickers/BTCUSD"
    try:
        res = requests.get(ticker_url)
        if res.status_code == 200:
            data = res.json()
            current_price = float(data['result']['close'])
            print(f"📊 Current BTCUSD Price: ${current_price}")
            
            # डमी RSI लॉजिक (डेमो टेस्टिंगसाठी)
            # प्रत्यक्षात जेव्हा RSI 30 च्या खाली किंवा 70 च्या वर जाईल तेव्हा मेसेज येईल
            print("\n🔍 Analysing Market Conditions...")
            print("👉 [DEMO LOG]: RSI Indicator is Normal (45.5). No Trade Executed.")
            print("🛡️ Safety: Real money is NOT used. Running in simulation mode.")
            
        else:
            print("⚠️ Unable to fetch market price.")
    except Exception as e:
        print(f"Error fetching ticker: {e}")

if __name__ == "__main__":
    if check_connection():
        run_paper_trading()
        
