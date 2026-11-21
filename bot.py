import requests, os

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

MONEDAS = ["BTC","ETH","SOL","NEAR","UNI","AAVE","TAO","INJ","TRUMP","XRP","LINK","AVAX","DOT","ADA","HUMA","SKY","VVV","QNT"]

def telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def get_data(market):
    r = requests.get(f"https://api.bitvavo.com/v2/ticker/24h?market={market}-EUR", timeout=10).json()
    if isinstance(r, list):
        r = r[0]
    price = float(r.get("price", 0))
    vol = float(r.get("volume", 0))
    if "priceChangePercent" in r:
        cambio = float(r["priceChangePercent"])
    elif "open" in r and float(r["open"]) != 0:
        cambio = (price - float(r["open"])) / float(r["open"]) * 100
    else:
        cambio = 0.0
    return price, cambio, vol

btc_price, btc_24h, _ = get_data("BTC")
print(f"BTC 24h: {btc_24h}%")
if btc_24h < -1.5:
    print("Freno BTC")
    exit()

for m in MONEDAS:
    if m == "BTC":
        continue
    try:
        price, cambio_24h, vol = get_data(m)
    except Exception as e:
        print(f"Error {m}: {e}")
        continue
    vs_btc = cambio_24h - btc_24h

    if vs_btc >= 3.0 and cambio_24h > 0:
        telegram(f"🟢 FUERTE - MIRAR {m}EUR | Precio: {price:.4f} € | 24h: {cambio_24h:+.2f}% | vs BTC: {vs_btc:+.2f}% | Vol: {vol:,.0f}€ | POSIBLE ENTRADA con limite por debajo")
    elif vs_btc >= 2.0 and cambio_24h > 0:
        telegram(f"🟡 TEMPRANO - MIRAR {m}EUR | Precio: {price:.4f} € | 24h: {cambio_24h:+.2f}% | vs BTC: {vs_btc:+.2f}% | Vol: {vol:,.0f}€ | Vigilar, no entrar todavia")
    else:
        print(f"No {m}: {cambio_24h:.2f}% vs BTC {vs_btc:.2f}%")
