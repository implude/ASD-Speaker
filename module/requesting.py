import requests, os, json

SN: str = os.environ['SN']
backend_url: str = os.environ['BACKEND_URL']

def request_stt(base64_encoded) -> str:
    param_dict: dict = {
        'SN': SN,
        'content': base64_encoded
    }
    param_json = json.dumps(param_dict)
    response: requests.Response = requests.post(backend_url, json=param_json)
    transcript: str = response.json()['transcript']

    return transcript

