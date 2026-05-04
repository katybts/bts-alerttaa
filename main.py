import time
import requests
import os

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

LINKS = {
    "21": "https://www.allaccess.com.ar/event/bts-21-de-octubre",
    "23": "https://www.allaccess.com.ar/event/bts-23-de-octubre",
    "24": "https://www.allaccess.com.ar/event/bts-24-de-octubre"
}

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

estado_prev = {fecha: False for fecha in LINKS}

def detectar_disponibilidad(texto):
    texto = texto.lower()

    # si dice comprar o disponible y NO agotado → posible disponibilidad real
    if ("comprar" in texto or "disponible" in texto) and "agotado" not in texto:
        return True
    return False

def detectar_sectores(texto):
    texto = texto.lower()
    sectores = []

    posibles = ["campo", "platea", "cabecera", "vip"]

    for s in posibles:
        if s in texto:
            sectores.append(s)

    return list(set(sectores))

while True:
    try:
        for fecha, link in LINKS.items():
            r = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
            texto = r.text

            disponible = detectar_disponibilidad(texto)

            if disponible and not estado_prev[fecha]:
                sectores = detectar_sectores(texto)

                mensaje = f"🚨 BTS\nENTRADAS DISPONIBLES - FECHA {fecha} 🔥\n"

                if sectores:
                    mensaje += "Sectores detectados: " + ", ".join(sectores) + "\n"

                mensaje += f"Entrar acá:\n{link}"

                enviar_telegram(mensaje)
                print(f"ALERTA en {fecha}")

                estado_prev[fecha] = True

            elif not disponible:
                estado_prev[fecha] = False
                print(f"{fecha}: sin disponibilidad")

    except Exception as e:
        print("Error:", e)

    time.sleep(300)