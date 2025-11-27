import requests
import random
import time
import os

# --- CONFIGURAÇÕES TELEGRAM ---
TOKEN = "8236724419:AAHIQP4SBRdhosHa0GK_03BUCkxmyw9ezhU"
MENSAGEM_CHEIA = "⚠️ A lixeira está cheia! Por favor, esvazie-a."
OGG_FILE = "lixeira_cheia.ogg"  # Seu arquivo de áudio .ogg com voz de personagem
USUARIOS_FILE = "usuarios.txt"  # Arquivo para salvar chat_ids dos usuários

# --- CONFIGURAÇÕES DA LIXEIRA ---
DISTANCE_THRESHOLD = 15  # Distância em cm para considerar cheia
TEMPO_LEITURA = 15        # Tempo entre leituras em segundos
mensagem_enviada = False  # Evita envio repetido enquanto lixeira cheia

# --- Carrega usuários já registrados ---
usuarios_registrados = []
if os.path.exists(USUARIOS_FILE):
    with open(USUARIOS_FILE, "r") as f:
        usuarios_registrados = [int(line.strip()) for line in f.readlines()]

print("Iniciando monitoramento simulado da lixeira...")

def registrar_usuarios():
    """Busca novas mensagens e registra usuários que interagirem com o bot."""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json().get("result", [])
        for update in updates:
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                if chat_id not in usuarios_registrados:
                    usuarios_registrados.append(chat_id)
                    print(f"Novo usuário registrado: {chat_id}")
                    # Salva no arquivo para persistência
                    with open(USUARIOS_FILE, "a") as f:
                        f.write(f"{chat_id}\n")

while True:
    # 1️⃣ Registra novos usuários
    registrar_usuarios()

    # 2️⃣ Simula a distância do sensor (0 a 30 cm)
    distancia = random.randint(0, 30)
    print(f"Distância simulada: {distancia} cm")

    # 3️⃣ Verifica se a lixeira está cheia
    if distancia <= DISTANCE_THRESHOLD and not mensagem_enviada:
        for chat_id in usuarios_registrados:
            # Envia mensagem de texto
            url_texto = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            params_texto = {"chat_id": chat_id, "text": MENSAGEM_CHEIA}
            response_texto = requests.get(url_texto, params=params_texto)
            if response_texto.status_code == 200:
                print(f"Mensagem de texto enviada para {chat_id}!")
            else:
                print(f"Erro ao enviar mensagem de texto para {chat_id}: {response_texto.text}")

            # Envia mensagem de voz (.ogg)
            url_voice = f"https://api.telegram.org/bot{TOKEN}/sendVoice"
            with open(OGG_FILE, 'rb') as voice_file:
                files = {'voice': voice_file}
                data = {"chat_id": chat_id}
                response_voice = requests.post(url_voice, files=files, data=data)
            if response_voice.status_code == 200:
                print(f"Mensagem de voz enviada para {chat_id}!")
            else:
                print(f"Erro ao enviar mensagem de voz para {chat_id}: {response_voice.text}")

        mensagem_enviada = True

    # 4️⃣ Reseta flag se a lixeira "foi esvaziada"
    elif distancia > DISTANCE_THRESHOLD and mensagem_enviada:
        mensagem_enviada = False
        print("Lixeira agora possui espaço disponível.")

    # Espera antes da próxima leitura
    time.sleep(TEMPO_LEITURA)
