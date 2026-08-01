import requests

BASE_URL = "https://api.india.delta.exchange"

def run_paper_trading():
    print("\n--- 🤖 PAPER TRADING BOT ACTIVE (PUBLIC DATA) ---")
    
    # BTCUSD चा थेट लाईव्ह रेट मिळवणे (यासाठी API Key ची गरज नाही)
    ticker_url = f"{BASE_URL}/v2/tickers/BTCUSD"
    try:
        res = requests.get(ticker_url)
        if res.status_code == 200:
            data = res.json()
            current_price = float(data['result']['close'])
            print(f"✅ Connection Successful!")
            print(f"📊 Current BTCUSD Price: ${current_price}")
            
            print("\n🔍 Analysing Market Conditions...")
            print("👉 [DEMO LOG]: RSI Indicator is Normal (45.5). No Trade Executed.")
            print("🛡️ Safety: Running in pure simulation mode.")
            
        else:
            print(f"❌ Connection Error: {res.text}")
    except Exception as e:
        print(f"Error fetching ticker: {e}")

if __name__ == "__main__":
    run_paper_trading()
    
