import requests

TOKEN = "8236724419:AAHIQP4SBRdhosHa0GK_03BUCkxmyw9ezhU"
CHAT_ID = "1568267415"
mensagem = "A lixeira está cheia!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensagem}"
response = requests.get(url)
print(response.status_code)  # deve ser 200
print(response.text)         # resposta completa do Telegram
