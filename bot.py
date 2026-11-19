import requests, time, os
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Añadido VVVEUR que te faltaba
MONEDAS = ["BTCEUR","SOLEUR","XRPEUR","ETHEUR","ADAEUR","LINKEUR","UNIEUR","DOGEEUR","AVAXEUR","NEAREUR","FETEUR","HBAREUR","XLMEUR","BCHEUR","SUIEUR","DOTEUR","QNTEUR","TRXEUR","RENDEREUR","LTCEUR","ALGOEUR","ETCEUR","AAVEEUR","POLEUR","TRUMPEUR","GRTEUR","CRVEUR","GRAMEUR","IMXEUR","BATEUR","CHZEUR","YFIEUR","AXSEUR","SUSHIEUR","COMPEUR","SKYEUR","INJEUR","TAOEUR","PEPEEUR","SHIBEUR","VVVEUR"]

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

def datos(moneda):
    base = moneda[:-3]
    market = f"{base}-EUR"
    url = f"https://api.bitvavo.com/v2/ticker/24h?market={market}"
    r = requests.get(url, timeout=10).json()
    d = r[0] if isinstance(r, list) else r
    precio = float(d['last'])
    apertura = float(d['open'])
    cambio24 = (precio - apertura) / apertura * 100
    # Volumen 24h en EUR, si no viene ponemos 0
    volumen = float(d.get('volume', 0)) * precio
    return precio, cambio24, volumen

def fmt(p):
    if p < 0.01:
        return f"{p:.8f}"
    else:
        return f"{p:.4f}"

# 1. Primero cogemos BTC para comparar todo contra él
try:
    precio_btc, cambio_btc, vol_btc = datos("BTCEUR")
    print(f"BTC referencia: {fmt(precio_btc)} € | 24h: {cambio_btc:+.2f}%")
except:
    cambio_btc = 0
    print("No se pudo coger BTC, uso 0")

for m in MONEDAS:
    try:
        p, c24, vol = datos(m)
        time.sleep(0.3)
        # 2. NUEVA FORMULA: fuerza relativa vs BTC
        fuerza = c24 - cambio_btc
        print(f"{m}: {fmt(p)} € | 24h: {c24:+.2f}% | vs BTC: {fuerza:+.2f}% | Vol: {vol:,.0f}€")

        # 3. NUEVOS UMBRALES: +3% vs BTC = FUERTE, +2% vs BTC = TEMPRANO, con volumen 400K€
        if fuerza >= 3 and vol >= 400000:
            enviar(f"🟢 FUERTE - MIRAR {m} | Precio: {fmt(p)} € | 24h: {c24:+.2f}% | vs BTC: {fuerza:+.2f}% | Vol: {vol:,.0f}€ | POSIBLE ENTRADA")
        elif fuerza >= 2 and vol >= 400000:
            enviar(f"🟡 TEMPRANO - MIRAR {m} | Precio: {fmt(p)} € | 24h: {c24:+.2f}% | vs BTC: {fuerza:+.2f}% | Vol: {vol:,.0f}€ | Vigilar, posicion pequeña")
    except Exception as e:
        print(f"Error en {m}: {e}")
        continue

print("Revision hecha")
