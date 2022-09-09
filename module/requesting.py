import requests, os, json

SN: str = os.environ['SN']
backend_url: str = os.environ['BACKEND_URL']

def request_stt(base64_encoded) -> str:
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'SN': SN
        }
    param_dict: dict = {
        "content": base64_encoded
    }
    param_json = json.dumps(param_dict)
    print(param_json)
    response: requests.Response = requests.post(backend_url+"/voice/stt", headers=headers,data=param_json)
    print(response.text)
    transcript: str = response.json()['transcript']

    return transcript


