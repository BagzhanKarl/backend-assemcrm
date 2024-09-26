import requests


def send_message(token, typing_time, to, body):
    url = "https://gate.whapi.cloud/messages/text"

    payload = {
        "typing_time": typing_time,
        "to": to,
        "body": body
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.text


# Example usage
token = "rmXQbivTFcJHwIpQtDWu58co0TaeqOCN"
response_text = send_message(token, 0, "77761174378", "Привет")
print(response_text)
