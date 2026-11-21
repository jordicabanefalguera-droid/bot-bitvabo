import requests, os

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

MONEDAS = ["BTC","ETH","SOL","NEAR","UNI","AAVE","TAO","INJ","TRUMP","XRP","LINK","AVAX","DOT","ADA","HUMA","SKY","VVV","QNT"]

def telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def get_data(market):
    # Precio actual
    r = requests.get(f"https://api.bitvavo.com/v2/ticker/price?market={market}-EUR", timeout=10).json()
    if isinstance(r, list):
        r = r[0]
    price = float(r.get("price", 0))

    # Vela de 1 dia: [timestamp, open, high, low, close, volume]
    c = requests.get(f"https://api.bitvavo.com/v2/{market}-EUR/candles?interval=1d&limit=2", timeout=10).json()
    # c puede venir como lista de listas
    last = c[-1]
    open_price = float(last[1])
    vol = float(last[5])
    cambio = (price - open_price) / open_price * 100 if open_price != 0 else 0.0
    return price, cambio, vol

btc_price, btc_24h, _ = get_data("BTC")
print(f"BTC precio: {btc_price} 24h: {btc_24h}%")
if btc_24h < -4.0:
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
