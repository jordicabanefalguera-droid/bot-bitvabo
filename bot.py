import requests, os

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

MONEDAS = ["BTC","ETH","SOL","NEAR","UNI","AAVE","TAO","INJ","TRUMP","XRP","LINK","AVAX","DOT","ADA","HUMA","SKY","VVV"]

def telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def get_ticker(market):
    r = requests.get(f"https://api.bitvavo.com/v2/ticker/24h?market={market}-EUR", timeout=10).json()
    if isinstance(r, list):
        r = r[0]
    return float(r["priceChangePercent"])

btc_24h = get_ticker("BTC")
if btc_24h < -1.5:
    print(f"BTC en {btc_24h}%, freno activado, no aviso")
    exit()

for m in MONEDAS:
    if m == "BTC":
        continue
    try:
        cambio_24h = get_ticker(m)
    except:
        continue
    vs_btc = cambio_24h - btc_24h
    if cambio_24h > 2.0 and vs_btc > 2.0:
        telegram(f"🐎 FUERTE - MIRAR {m}EUR\n24h: +{cambio_24h:.2f}%\nvs BTC: +{vs_btc:.2f}%\nBTC 24h: {btc_24h:.2f}%\nRevisa en 15m si sigue verde antes de entrar")
        print(f"Aviso {m}")
