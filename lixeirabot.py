import serial
import requests
import time

# --- CONFIGURAÇÕES TELEGRAM ---
TOKEN = "8236724419:AAHIQP4SBRdhosHa0GK_03BUCkxmyw9ezhU"
CHAT_ID = "1568267415"
mensagem = "A lixeira está cheia!"

# --- CONFIGURAÇÕES ARDUINO ---
PORTA_SERIAL = "COM3"  # substitua pela porta do seu Arduino
BAUD_RATE = 9600       # deve ser igual ao usado no Arduino
DISTANCE_THRESHOLD = 15  # distância limite em cm

# Inicializa conexão serial
try:
    arduino = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)  # espera o Arduino iniciar
except Exception as e:
    print("Erro ao conectar com Arduino:", e)
    exit()

print("Monitorando lixeira...")

mensagem_enviada = False  # controla para não enviar repetidamente

while True:
    try:
        # Lê a linha enviada pelo Arduino
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            try:
                distancia = float(linha)
                print(f"Distância lida: {distancia} cm")

                # Verifica se a lixeira está cheia
                if distancia <= DISTANCE_THRESHOLD and not mensagem_enviada:
                    # Envia mensagem para Telegram
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    params = {"chat_id": CHAT_ID, "text": mensagem}
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        print("Mensagem enviada com sucesso!")
                        mensagem_enviada = True  # evita enviar várias vezes seguidas
                    else:
                        print("Falha ao enviar mensagem:", response.text)

                # Reseta flag se a lixeira foi esvaziada
                elif distancia > DISTANCE_THRESHOLD and mensagem_enviada:
                    mensagem_enviada = False

            except ValueError:
                print("Valor inválido recebido do Arduino:", linha)

    except KeyboardInterrupt:
        print("Encerrando monitoramento...")
        break
