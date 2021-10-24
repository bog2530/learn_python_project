import requests

from key import headers # noqa


url = "https://microsoft-translator-text.p.rapidapi.com/translate"

querystring = {"to": "ru", "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}


def translate(text):
    payload = '[{\"Text\": ' + f'\"{text}\"' + '}]'
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    return response.text


text = "THE AQUARIUM is the headquarters of the GRU - Soviet Military Intelligence." + " "

if __name__ == "__main__":
    print(translate(text.encode('utf-8'))[78:-16])
