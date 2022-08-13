import requests
import json
url = "http://38.130.130.45:9595/invoice-ocr/"
file = open('1.pdf', 'rb')

payload=json.dumps({'lang': 'eng','document':file.read().decode("utf-8")})

headers = {
    "Content-Type":"application/json"
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


