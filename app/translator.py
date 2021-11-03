import requests

from app.key import headers

url = "https://microsoft-translator-text.p.rapidapi.com/translate"

querystring = {"to": "ru", "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}


def translate(text):
    payload = [{"Text": f"{text}"}]
    response = requests.post(url, json=payload, headers=headers, params=querystring)
    return response.json()[0]['translations'][0]['text']
