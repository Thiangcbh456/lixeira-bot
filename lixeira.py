import requests

TOKEN = "8236724419:AAHIQP4SBRdhosHa0GK_03BUCkxmyw9ezhU"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(url)
print(response.json())

