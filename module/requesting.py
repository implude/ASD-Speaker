from sre_constants import SUCCESS
from unittest import result
import requests, os, json

SN: str = os.environ['SN']
backend_url: str = os.environ['BACKEND_URL']

class return_value:
    def __init__(self, transcript, err) -> None:
        self.transcript = transcript
        self.err = err

def request_stt(base64_encoded) -> return_value:
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'SN': SN
        }
    param_dict: dict = {
        "content": base64_encoded
    }
    param_json = json.dumps(param_dict)
    response: requests.Response = requests.post(backend_url+"/voice/stt", headers=headers,data=param_json)
    result = response.json()
    if result["sucess"] != "true":
        err = True
        transcript: str = None
    else:
        err = False
        transcript: str = response.json()['result'][0]["transcript"]
    return return_value(transcript=transcript,err=err)


        


