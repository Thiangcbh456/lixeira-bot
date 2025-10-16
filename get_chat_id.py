import requests

TOKEN = "8236724419:AAHIQP4SBRdhosHa0GK_03BUCkxmyw9ezhU"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

try:
    response = requests.get(url)
    print(response.status_code)  # deve mostrar 200
    print(response.text)         # mostra o JSON retornado
except Exception as e:
    print("Erro ao conectar:", e)
