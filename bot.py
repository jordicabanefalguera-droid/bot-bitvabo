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
    # Si viene el campo bueno, usarlo
    if "priceChangePercent" in r:
        return float(r["priceChangePercent"])
    # Si no, calcularlo desde precio y apertura
    if "price" in r and "open" in r:
        price = float(r["price"])
        open_price = float(r["open"])
        return (price - open_price) / open_price * 100
    # Si viene priceChange en euros, calcularlo
    if "priceChange" in r and "price" in r:
        return float(r["priceChange"]) / float(r["price"]) * 100
    print(f"Respuesta rara {market}: {r}")
    return 0.0

btc_24h = get_ticker("BTC")
print(f"BTC 24h: {btc_24h}%")
if btc_24h < -1.5:
    print(f"BTC en {btc_24h}%, freno activado, no aviso")
    exit()

for m in MONEDAS:
    if m == "BTC":
        continue
    try:
        cambio_24h = get_ticker(m)
    except Exception as e:
        print(f"Error {m}: {e}")
        continue
    vs_btc = cambio_24h - btc_24h
    if cambio_24h > 2.0 and vs_btc > 2.0:
        telegram(f"🐎 FUERTE - MIRAR {m}EUR\n24h: +{cambio_24h:.2f}%\nvs BTC: +{vs_btc:.2f}%\nBTC 24h: {btc_24h:.2f}%\nRevisa en 15m si sigue verde antes de entrar")
        print(f"Aviso {m}")
