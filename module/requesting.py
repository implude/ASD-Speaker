import requests, os, json

SN: str = os.environ['SN']
backend_url: str = os.environ['BACKEND_URL']

class return_value:
    def __init__(self, transcript, err) -> None:
        self.transcript = transcript
        self.err = err

def request_stt(base64_encoded) -> return_value:
    headers: dict = {
        'Content-Type': 'application/json; charset=utf-8',
        'SN': SN
        }
    param_dict: dict = {
        "content": base64_encoded
    }
    param_json = json.dumps(param_dict)
    
    response: requests.Response = requests.post(backend_url+"/voice/stt", headers=headers,data=param_json)
    print(response.text)
    result: dict = response.json()
    
    if result["success"]:
        
        transcript: str = response.json()['result'][0]["transcript"]
    else:
        transcript: str = None
    return return_value(transcript=transcript,err=not result["success"])

def request_start_study_mode():
    headers: dict = {
        'Content-Type': 'application/json; charset=utf-8',
        'SN': SN
        }
    response: requests.Response = requests.get(backend_url+"/study_mode", headers=headers)
    print(response.text)
    result: dict = response.json()
    return result["success"]



        


