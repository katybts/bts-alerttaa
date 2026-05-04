import time
import requests
import os
import re

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL = "https://www.allaccess.com.ar/event/bts"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# guardamos estado por fecha
estado_fechas = {}

def detectar_estado(bloque):
    bloque = bloque.lower()
    if "comprar" in bloque or "disponible" in bloque:
        return "disponible"
    elif "agotado" in bloque:
        return "agotado"
    return "sin info"

while True:
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        html = r.text.lower()

        # 🔎 buscar bloques que contengan fechas
        bloques = re.findall(r"(21.*?)(?=22|23|24|$)", html, re.DOTALL) + \
                  re.findall(r"(23.*?)(?=24|$)", html, re.DOTALL) + \
                  re.findall(r"(24.*)", html, re.DOTALL)

        for bloque in bloques:
            for fecha in ["21", "23", "24"]:
                if fecha in bloque:
                    nuevo_estado = detectar_estado(bloque)
                    viejo_estado = estado_fechas.get(fecha, "desconocido")

                    if nuevo_estado != viejo_estado:
                        if nuevo_estado == "disponible":
                            mensaje = f"🚨 BTS\nENTRADAS DISPONIBLES EN FECHA {fecha} 🔥\n{URL}"
                        elif nuevo_estado == "agotado":
                            mensaje = f"❌ BTS\nFECHA {fecha} AGOTADA\n{URL}"
                        else:
                            mensaje = f"⚠️ BTS\nCAMBIO EN FECHA {fecha}\n{URL}"

                        enviar_telegram(mensaje)
                        print(f"Cambio en {fecha}: {viejo_estado} → {nuevo_estado}")
                        estado_fechas[fecha] = nuevo_estado

    except Exception as e:
        print("Error:", e)

    time.sleep(300)