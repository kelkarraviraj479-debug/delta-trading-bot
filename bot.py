import os
import pandas as pd
import requests
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BASE_URL = "https://api.india.delta.exchange"


def send_telegram_message(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Telegram Exception: {e}")


def get_delta_candles(symbol="BTCUSD", resolution="1h", limit=50):
    # Delta Exchange API वरून OHLCV डेटा घेणे
    url = f"{BASE_URL}/v2/chart/history?symbol={symbol}&resolution={resolution}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            df = pd.DataFrame(data["result"])
            # 'close' किंमती Float मध्ये रूपांतरित करणे
            df["close"] = df["close"].astype(float)
            return df
    except Exception as e:
        print(f"Candle Data Fetch Error: {e}")
    return None


def run_paper_trading(symbol="BTCUSD"):
    df = get_delta_candles(symbol=symbol, resolution="1h", limit=50)

    if df is None or df.empty:
        print("❌ Delta API Data Empty")
        return

    # १. RSI (14) कॅल्क्युलेट करणे
    rsi_calc = RSIIndicator(close=df["close"], window=14)
    df["RSI"] = rsi_calc.rsi()

    # २. EMA (9) कॅल्क्युलेट करणे
    ema_calc = EMAIndicator(close=df["close"], window=9)
    df["EMA9"] = ema_calc.ema_indicator()

    price = df["close"].iloc[-1]
    rsi = df["RSI"].iloc[-1]
    ema = df["EMA9"].iloc[-1]

    # ३. स्मार्ट ट्रेडिंग लॉजिक (Paper Trade Signals)
    if rsi < 35:
        signal = "🟢 LONG ENTRY (Oversold Zone)"
        tp = price * 1.02  # 2% Take Profit
        sl = price * 0.99  # 1% Stop Loss
    elif rsi > 65:
        signal = "🔴 SHORT ENTRY (Overbought Zone)"
        tp = price * 0.98
        sl = price * 1.01
    elif price > ema and rsi > 50:
        signal = "🟢 BULLISH TREND (Hold Long)"
        tp, sl = price * 1.015, price * 0.992
    elif price < ema and rsi < 50:
        signal = "🔴 BEARISH TREND (Hold Short)"
        tp, sl = price * 0.985, price * 1.008
    else:
        signal = "🟡 NO TRADE (Market Neutral)"
        tp, sl = 0, 0

    # ४. टेलीग्राम मेसेज
    msg = (
        f"🤖 *Delta India Crypto Bot*\n\n"
        f"🪙 *Pair:* {symbol}\n"
        f"💵 *Current Price:* ${price:,.2f}\n"
        f"📊 *RSI (14):* {rsi:.2f}\n"
        f"📈 *EMA (9):* ${ema:,.2f}\n\n"
        f"🎯 *Signal:* {signal}\n"
    )

    if tp > 0 and sl > 0:
        msg += f"🎯 *Target TP:* ${tp:,.2f}\n🛡️ *Stop Loss:* ${sl:,.2f}\n"

    msg += "\n_📝 Mode: Paper Trading_"

    print(msg)
    send_telegram_message(msg)


if __name__ == "__main__":
    run_paper_trading("BTCUSD")
    run_paper_trading("ETHUSD")
    
