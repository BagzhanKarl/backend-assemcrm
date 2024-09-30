import requests

def send_text_message(token, chat_id, text):
    url = "https://gate.whapi.cloud/messages/text"

    payload = {
        "typing_time": 0,
        "to": f"{chat_id}",
        "body": f"{text}"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.sent

def send_image_message(token, chat_id, media):
    url = "https://gate.whapi.cloud/messages/image"

    payload = {
        "to": f"{chat_id}",
        "media": f"{media}"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.sent

def react_to_message_token(token, message_id, emoji):

    url = f"https://gate.whapi.cloud/messages/{message_id}/reaction"

    payload = {"emoji": f"{emoji}"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }

    response = requests.put(url, json=payload, headers=headers)

    print(response.text)