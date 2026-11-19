import requests, time, os
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MONEDAS = ["BTCEUR","SOLEUR","XRPEUR","ETHEUR","ADAEUR","LINKEUR","UNIEUR","DOGEEUR","AVAXEUR","NEAREUR","FETEUR","HBAREUR","XLMEUR","BCHEUR","SUIEUR","DOTEUR","QNTEUR","TRXEUR","RENDEREUR","LTCEUR","ALGOEUR","ETCEUR","AAVEEUR","POLEUR","TRUMPEUR","GRTEUR","CRVEUR","GRAMEUR","IMXEUR","BATEUR","CHZEUR","YFIEUR","AXSEUR","SUSHIEUR","COMPEUR","SKYEUR","INJEUR","TAOEUR","PEPEEUR","SHIBEUR"]
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
    return precio, cambio24
def fmt(p):
    if p < 0.01:
        return f"{p:.8f}"
    else:
        return f"{p:.4f}"
for m in MONEDAS:
    try:
        p, c24 = datos(m)
        time.sleep(0.3)
        print(f"{m}: {fmt(p)} € | 24h: {c24:+.2f}%")
        if c24 >= 5:
            enviar(f"VERDE - MIRAR {m} | Precio: {fmt(p)} € | 24h: {c24:+.2f}% | POSIBLE ENTRADA")
        elif c24 >= 3:
            enviar(f"REBOTE - MIRAR {m} | Precio: {fmt(p)} € | 24h: {c24:+.2f}% | Rebote bueno, posicion pequena")
    except Exception as e:
        print(f"Error en {m}: {e}")
        continue
print("Revision hecha")
