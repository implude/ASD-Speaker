import requests, os, json

SN: str = os.environ['SN']
backend_url: str = os.environ['BACKEND_URL']

class return_value: # 리턴 값 전달을 위한 객체
    def __init__(self, transcript, err) -> None:
        self.transcript = transcript
        self.err = err

def request_stt(base64_encoded) -> return_value: # 서버에 STT 요청
    headers: dict = { # 요청 헤더 변수 
        'Content-Type': 'application/json; charset=utf-8',
        'SN': SN
        }
    param_dict: dict = { # 요청 내용 Dictionary 변수
        "content": base64_encoded
    }
    param_json = json.dumps(param_dict) # 요청 내용 JSON 변수
    
    response: requests.Response = requests.post(backend_url+"/voice/stt", headers=headers,data=param_json) # 요청 전송 후 데이터를 response 변수에 저장
    print(response.text) # 응답 내용 출력
    result: dict = response.json() # 응답 내용을 JSON 형식에서 Dictionary로 변환
    
    if result["success"]:
        
        transcript: str = response.json()['result'][0]["transcript"] # 응답 내용에서 가장 높은 확률의 transcript 부분만 추출
    else:
        transcript: str = None
    return return_value(transcript=transcript,err=not result["success"]) # 에러 리턴

def request_start_study_mode():
    headers: dict = {
        'Content-Type': 'application/json; charset=utf-8',
        'SN': SN
        }
    response: requests.Response = requests.get(backend_url+"/study_mode", headers=headers)
    print(response.text)
    result: dict = response.json()
    return result["success"]



        


