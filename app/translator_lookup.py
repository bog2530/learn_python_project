# -*- coding: utf-8 -*-
import requests

from app.key import headers

url_lookup = "https://microsoft-translator-text.p.rapidapi.com/Dictionary/Lookup"
querystring_lookup = {"to": "en", "api-version": "3.0", "from": "ru"}


def translate_lookup(text):
    payload = [{"Text": f"{text}"}]
    response = requests.post(url_lookup, json=payload, headers=headers, params=querystring_lookup)
    return response.json()[0]['translations']
