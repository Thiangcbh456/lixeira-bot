import requests
import time
import os
import serial
import serial.tools.list_ports

# --- CONFIGURAÇÕES TELEGRAM ---
TOKEN = "8236724419:AAHIQP4SBRdhosHa0GK_03BUCkxmyw9ezhU"
MENSAGEM_CHEIA = "⚠️ A lixeira está cheia! Por favor, esvazie-a."
OGG_FILE = "lixeira_cheia.ogg"
USUARIOS_FILE = "usuarios.txt"

# --- CONFIGURAÇÕES ARDUINO ---
BAUD_RATE = 9600

# --- ESTADO DA LIXEIRA ---
lixeira_cheia = False
ultimo_alerta = 0
INTERVALO_ALERTA = 5  # segundos entre notificações enquanto continua cheia

# --- CARREGAR USUÁRIOS EXISTENTES ---
usuarios_registrados = []
if os.path.exists(USUARIOS_FILE):
    with open(USUARIOS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    usuarios_registrados.append(int(line))
                except ValueError:
                    pass

print("Iniciando monitoramento da lixeira (Arduino + Bot Telegram)...")

# ------------------------------------------------------------ #
#  FUNÇÕES AUXILIARES
# ------------------------------------------------------------ #

def encontrar_porta_arduino(baudrate=9600, timeout=1):
    """Tenta identificar automaticamente a porta serial do Arduino."""
    portas = serial.tools.list_ports.comports()
    if not portas:
        print("Nenhuma porta serial encontrada.")
        return None

    print("Portas encontradas:")
    for porta in portas:
        print(f" - {porta.device} | {porta.description}")

    for porta in portas:
        desc = porta.description.lower()
        if any(x in desc for x in ["arduino", "ch340", "usb-serial", "usb serial", "cdc"]):
            try:
                ser = serial.Serial(porta.device, baudrate, timeout=timeout)
                ser.close()
                print(f"Possível Arduino encontrado: {porta.device}")
                return porta.device
            except Exception:
                pass

    print("Tentando abrir portas manualmente...")
    for porta in portas:
        try:
            ser = serial.Serial(porta.device, baudrate, timeout=timeout)
            ser.close()
            print(f"Porta serial utilizável: {porta.device}")
            return porta.device
        except:
            continue

    print("Não foi possível encontrar o Arduino automaticamente.")
    return None


def registrar_usuarios():
    """Busca novas mensagens e registra quem interagir com o bot."""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        print(f"Erro chamando getUpdates: {e}")
        return

    if response.status_code == 200:
        updates = response.json().get("result", [])
        for update in updates:
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                if chat_id not in usuarios_registrados:
                    usuarios_registrados.append(chat_id)
                    print(f"Novo usuário registrado: {chat_id}")
                    with open(USUARIOS_FILE, "a") as f:
                        f.write(f"{chat_id}\n")
    else:
        print(f"Erro no getUpdates: {response.text}")


def enviar_alerta_lixeira_cheia():
    """Envia texto e (se existir) áudio para todos os usuários cadastrados."""
    if not usuarios_registrados:
        print("Nenhum usuário registrado; alerta não enviado.")
        return

    for chat_id in usuarios_registrados:
        # Envia texto
        url_texto = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params_texto = {"chat_id": chat_id, "text": MENSAGEM_CHEIA}
        try:
            r_txt = requests.get(url_texto, params=params_texto, timeout=5)
            if r_txt.status_code == 200:
                print(f"Mensagem enviada para {chat_id}")
            else:
                print(f"Erro ao enviar texto: {r_txt.text}")
        except Exception as e:
            print(f"Erro de envio (texto): {e}")

        # Envia voz opcional
        if os.path.exists(OGG_FILE):
            url_voice = f"https://api.telegram.org/bot{TOKEN}/sendVoice"
            try:
                with open(OGG_FILE, 'rb') as voice_file:
                    files = {'voice': voice_file}
                    data = {'chat_id': chat_id}
                    r_voice = requests.post(url_voice, files=files, data=data, timeout=10)
                if r_voice.status_code == 200:
                    print(f"Mensagem de voz enviada para {chat_id}")
                else:
                    print(f"Erro voz: {r_voice.text}")
            except Exception as e:
                print(f"Erro enviar voz: {e}")
        else:
            print(f"Arquivo de voz '{OGG_FILE}' não encontrado.")


# ------------------------------------------------------------ #
#  LOOP PRINCIPAL
# ------------------------------------------------------------ #

def main():
    global lixeira_cheia, ultimo_alerta

    porta = encontrar_porta_arduino(baudrate=BAUD_RATE, timeout=1)
    if porta is None:
        print("Nenhum Arduino encontrado. Verifique o cabo/porta.")
        return

    print(f"Conectando ao Arduino na porta {porta}...")
    try:
        ser = serial.Serial(porta, BAUD_RATE, timeout=0.5)
        time.sleep(3)                # tempo para reinicializar
        ser.reset_input_buffer()
        print("Arduino pronto para leitura.\n")
    except Exception as e:
        print(f"Erro ao abrir {porta}: {e}")
        return

    print("Monitorando leituras em tempo real (CTRL+C para sair)...")

    try:
        buffer_incompleto = ""
        while True:
            registrar_usuarios()

            # lê todos os bytes disponíveis
            dados = ser.read(ser.in_waiting or 1).decode("utf-8", errors="ignore")
            if dados:
                buffer_incompleto += dados
                # separa por linhas completas
                linhas = buffer_incompleto.splitlines()

                # se a última linha não termina com \n, guarda-a para completar no próximo ciclo
                if not buffer_incompleto.endswith("\n"):
                    buffer_incompleto = linhas.pop() if linhas else ""
                else:
                    buffer_incompleto = ""

                for linha in linhas:
                    linha = linha.strip()
                    if not linha:
                        continue

                    # --- Leituras contínuas ---
                    if linha.startswith("DISTANCIA:"):
                        try:
                            valor_str = (
                                linha.split("DISTANCIA:")[-1]
                                .replace("cm", "")
                                .strip()
                            )
                            valor = float(valor_str)
                            print(f"Distância: {valor:.2f} cm")
                        except Exception:
                            print(f"Leitura inválida: {linha}")
                        continue

                    # --- Eventos de estado ---
                    if linha == "LIXEIRA_CHEIA" and not lixeira_cheia:
                        lixeira_cheia = True
                        print("→ A lixeira está CHEIA. Enviando alerta...")
                        enviar_alerta_lixeira_cheia()
                        ultimo_alerta = time.time()
                        continue

                    if linha == "LIXEIRA_OK" and lixeira_cheia:
                        lixeira_cheia = False
                        print("→ A lixeira voltou ao normal (tem espaço).")
                        continue

            # 🔁 Reenvio periódico enquanto continua cheia
            if lixeira_cheia:
                agora = time.time()
                if agora - ultimo_alerta >= INTERVALO_ALERTA:
                    print("→ Lixeira ainda CHEIA. Reenviando alerta ao Telegram...")
                    enviar_alerta_lixeira_cheia()
                    ultimo_alerta = agora

            time.sleep(0.02)  # ciclo rápido (~50 Hz)

    except KeyboardInterrupt:
        print("\nEncerrando monitoramento...")
    finally:
        try:
            ser.close()
            print("Porta serial fechada.")
        except:
            pass


if __name__ == "__main__":
    main()