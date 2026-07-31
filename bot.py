import os
import hmac
import hashlib
import time
import requests
import json

# GitHub Secrets मधून API Keys वाचणे
API_KEY = os.environ.get("DELTA_API_KEY")
API_SECRET = os.environ.get("DELTA_API_SECRET")
BASE_URL = "https://api.delta.exchange"

def generate_signature(method, path, payload="", timestamp=""):
    signature_data = method + timestamp + path + payload
    message = bytes(signature_data, 'utf-8')
    secret = bytes(API_SECRET, 'utf-8')
    return hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()

def get_headers(method, path, payload=""):
    timestamp = str(int(time.time()))
    signature = generate_signature(method, path, payload, timestamp)
    return {
        'api-key': API_KEY,
        'signature': signature,
        'timestamp': timestamp,
        'Content-Type': 'application/json'
    }

def run_bot():
    print("--- Delta Exchange Auto Trading Bot Active ---")
    path = "/v2/wallet/balances"
    headers = get_headers('GET', path)
    
    try:
        response = requests.get(BASE_URL + path, headers=headers)
        if response.status_code == 200:
            print("Successfully Connected to Delta Exchange!")
            print("Wallet Data:", response.json())
        else:
            print(f"Connection Error: {response.text}")
    except Exception as e:
        print(f"Execution Error: {e}")

if __name__ == "__main__":
    run_bot()
  
