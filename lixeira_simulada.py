import requests
import random
import time

# Configurações Telegram
TOKEN = "8236724419:AAHIQP4SBRdhosHa0GK_03BUCkxmyw9ezhU"
CHAT_ID = "1568267415"
mensagem = "A lixeira está cheia!"

DISTANCE_THRESHOLD = 15  # limite em cm

mensagem_enviada = False

while True:
    distancia = random.randint(0, 30)
    print(f"Distância simulada: {distancia} cm")

    if distancia <= DISTANCE_THRESHOLD and not mensagem_enviada:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": mensagem}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Mensagem enviada para Telegram!")
            mensagem_enviada = True
        else:
            print("Erro ao enviar mensagem:", response.text)

    elif distancia > DISTANCE_THRESHOLD and mensagem_enviada:
        mensagem_enviada = False

    time.sleep(2)
