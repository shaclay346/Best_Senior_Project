import requests
import json

url = "https://api.dictionaryapi.dev/api/v2/entries/en/test"


response = requests.request("GET", url)
text = json.loads(response.text)
print(text[0]["meanings"][0]["definitions"][0]["definition"])

print("bruh")
