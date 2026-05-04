import time
import requests

# 🔐 PEGÁ TU TOKEN ENTRE LAS COMILLAS
import os

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL = "https://www.allaccess.com.ar/event/bts"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# 🔔 MENSAJE DE PRUEBA (para confirmar que funciona)
enviar_telegram("✅ Bot funcionando correctamente")

ultimo = ""

while True:
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        texto = r.text.lower()

        keywords = ["21", "24", "comprar", "entradas", "disponible"]

        if any(k in texto for k in keywords):
            if texto != ultimo:
                enviar_telegram("🚨 BTS: CAMBIO DETECTADO\nEntrá YA:\n" + URL)
                print("ALERTA ENVIADA")
                ultimo = texto
            else:
                print("Sin cambios")
        else:
            print("Nada aún")

    except Exception as e:
        print("Error:", e)

    time.sleep(300)  # ⏱ cada 5 minutos
