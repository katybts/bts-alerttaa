import time
import requests
import os

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL = "https://www.allaccess.com.ar/event/bts"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# estado anterior de cada fecha
estado_fechas = {
    "21": "desconocido",
    "23": "desconocido",
    "24": "desconocido"
}

def detectar_estado(texto, fecha):
    if fecha in texto:
        if "comprar" in texto or "disponible" in texto:
            return "disponible"
        elif "agotado" in texto:
            return "agotado"
    return "sin info"

while True:
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        texto = r.text.lower()

        for fecha in estado_fechas.keys():
            nuevo_estado = detectar_estado(texto, fecha)
            viejo_estado = estado_fechas[fecha]

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
            else:
                print(f"Sin cambios en {fecha}")

    except Exception as e:
        print("Error:", e)

    time.sleep(300)