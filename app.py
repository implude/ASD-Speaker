from multiprocessing.resource_sharer import stop
from dotenv import load_dotenv
load_dotenv()

from time import time
import speech_recognition as sr
import datetime, base64, time, socketio, os

from module import requesting, language_process, board_controll
import pygame

pygame.mixer.init()

global volume

volume = 0.80

global sequence
global sequence_dict

sequence: int = 0
sequence_dict: dict = {
    "IDLE": 0,
    "WAKE_UP": 1,
    "LISTENING": 2,
    "SPEAKING": 3,
    "WAITING_NFC": 4
}

global white_noise_index
global white_noise_list
global white_playing

white_noise_index = 0
white_noise_list = [
    pygame.mixer.Sound("./audio/fire_sound.wav"),
    pygame.mixer.Sound("./audio/rain_sound.wav"),
    pygame.mixer.Sound("./audio/library_sound.wav")
]
white_noise_playing = False

global led_color
global led_on
global led_bright

led_bright = 100
led_on = True

led_color = "ffffff"

audio_dict: dict = {
    
    "네 공부 모드를 시작할까요?": "shall_we_start_study_mode.wav",
    "휴대폰을 올려 놓으셨군요 공부 모드를 시작합니다": "start_study_mode_with_phone.wav",
    "휴대폰을 올려 인식되지 않아 공부 모드가 종료되었어요": "phone_not_found_study_stop.wav",
    "네 휴대폰을 올려 놓으시면 공부 모드를 시작할게요": "start_study_mode.wav",
    "네 공부모드를 종료할게요": "stop_study_mode.wav",
    "네 무었을 도와드릴까요?": "what_can_i_do.wav",
    "네 백색소음을 재생할게요": "play_white_noise.wav",
    "네 백색소음을 변경할게요": "change_white_noise.wav",
    "네 백색소음을 종료했어요": "stop_white_noise.wav",
    "네 볼륨을 줄일게요": "decrease_volume.wav",
    "네 볼륨을 키울게요": "increase_volume.wav",
    "현재 볼륨이 최대 입니다": "volume_max.wav",
    "현재 볼륨이 최소 입니다": "volume_min.wav",
    "네 볼륨을 최대로 키울게요": "increase_volume_max.wav",
    "네 볼륨을 최소로 줄일게요": "decrease_volume_min.wav",
    "네 LED 밝기를 줄일게요": "decrease_led.wav",
    "네 LED 밝기를 높일게요": "increase_led.wav",
    "네 LED를 켤게요": "turn_on_led.wav",
    "네 LED를 끌게요": "turn_off_led.wav",
    "이해하지 못했어요 다시 한번 말해주세요": "i_dont_understand.wav",
    "30분 미만": "30min.wav",
    "1시간 미만": "under1.wav",
    1: "1.wav",
    2: "2.wav",
    3: "3.wav",
    4: "4.wav",
    5: "5.wav",
    6: "6.wav",
    7: "7.wav",


    }

def waiting_for_idle() -> None:
    while sequence != 0:
        time.sleep(0.15)
    return

# SocketIO Connection Handeler

sio = socketio.Client()
sio.connect(os.environ['BACKEND_URL'], wait_timeout=10)
def on_connect():
    print('Socket connected')
    sio.emit('SN',os.environ['SN'])

def on_disconnect():
    print('Socket disconnected')

def on_reconnect():
    print('Socket reconnect')

def on_nfc_on_message(data):
    print(data)
    waiting_for_idle()
    talk('휴대폰을 올려 놓으셨군요 공부 모드를 시작합니다')
    sio.emit('study', 'study start')

def on_nfc_off_message(data):
    waiting_for_idle()
    talk('휴대폰을 올려 인식되지 않아 공부 모드가 종료되었어요')
    sio.emit('study', 'study stop')

def on_led_color_message(data):
    global sequence
    global led_color
    global led_on
    data = data.replace('#', '')
    if len(data) == 6:
        print('LED Color Changed')
        led_color = data
        board_controll.change_led_color(data)
def on_led_bright_change_message(data):
    global sequence
    global led_on
    global led_bright
    led_on = True
    led_bright = int(data)*10
    print('LED Brightness Changed: '+ str(led_bright))
    board_controll.change_led_bright(led_bright)

def on_volume_message(data):
    change_volume(volume_val=data/10)
    print("Volume Changed by Remote: " + str(data))

def on_white_noise_message(data):
    print('White Noise Changed: ' + str(data))
sio.on('connect', on_connect)
sio.on('disconnect', on_disconnect)
sio.on('reconnect', on_reconnect)
sio.on('nfc_on', on_nfc_on_message)
sio.on('nfc_off', on_nfc_off_message)
sio.on('LED_color', on_led_color_message)
sio.on('LED_bright', on_led_bright_change_message)
sio.on('volume', on_volume_message)
sio.on('white_noise', on_white_noise_message)

def change_volume(volume_val):
    global volume
    volume = volume_val
    if white_noise_index != 0:
        play_white_noise(white_noise_index-1)


def talk(text) -> None:
    global sequence
    ex_sequence: int = sequence
    sequence = sequence_dict["SPEAKING"]
    print("세리: "+text)
    sound = pygame.mixer.Sound("audio/" + audio_dict[text])
    sound.set_volume(volume)
    channal = sound.play() 
    while channal.get_busy():
        time.sleep(0.01)
    sequence = ex_sequence

def queue_white_noise():
    global white_noise_index
    if white_noise_index == 0:
        white_noise_index = 1
    else:
        if white_noise_index == 3:
            white_noise_index = 1
        else:
            white_noise_index += 1
    play_white_noise(white_noise_index-1)


def play_white_noise(index):
    global white_noise_list
    stop_white_noise()
    white_noise_list[index].set_volume(volume)
    white_noise_list[index].play(-1,fade_ms = 1000)

def stop_white_noise():
    global white_noise_list
    for i in range(len(white_noise_list)):
        white_noise_list[i].stop()

def take_command(): # 음성 명령 인식 함수
    if os.environ["CLI_MODE"] == "0":
        with sr.Microphone() as source: # Michrophone 함수로 받아온 리턴 객체를 source 변수에 저장
            print("prepareing to listen...")
            rn.adjust_for_ambient_noise(source) # 소스로 부터 받아온 데이터 기반으로 적응형 노이즈 제거
            print('listening...')
            voice = rn.listen(source) # source로 부터 음성 데이터를 voice 변수에 저장
            print('encoding...')
            base64_encoded_voice: str = base64.b64encode(voice.get_wav_data()).decode('utf-8') # voice를 PCM형삭으로 변환후 base64로 인코딩한후 다시 전송을 위해 utf8로 디코딩
            print('recognizing...')
            transcript: str = requesting.request_stt(base64_encoded_voice) # 반환된 텍스트를 transcript 변수에 저장
            print('processing...')
            return transcript
    else:
        return requesting.return_value(input("명령을 입력하세요: "), False)

def main() -> None:
    global sequence
    while True:
        transcript: requesting.return_value = take_command()
        if transcript.err:
            talk("대화를 처리하는 과정에서 문제가 발생했습니다")
            continue
        if language_process.is_wake_up_word(transcript.transcript):
            waiting_for_idle()
            sequence = sequence_dict["WAKE_UP"]
            talk('네 무었을 도와드릴까요?')
            sequence = sequence_dict["LISTENING"]
            understand = False
            while not understand:
                transcript: requesting.return_value = take_command()
                if transcript.err:
                    talk("대화를 처리하는 과정에서 문제가 발생했습니다")
                    sequence = sequence_dict["IDLE"]
                    continue
                if language_process.is_study_mode(transcript.transcript):
                    if language_process.is_start_word(transcript.transcript):
                        talk("네 휴대폰을 올려 놓으시면 공부 모드를 시작할게요")
                        understand = True
                    elif language_process.is_stop_word(transcript.transcript):
                        talk("네 공부모드를 종료할게요")
                        understand = True
                    else:
                        talk("이해하지 못했어요 다시 한번 말해주세요")
                elif language_process.is_white_noise(transcript.transcript):
                    
                    if language_process.is_change_word(transcript.transcript):
                        talk("네 백색소음을 변경할게요")
                        queue_white_noise()
                        understand = True
                    elif language_process.is_stop_word(transcript.transcript):
                        stop_white_noise()
                        talk("네 백색소음을 종료했어요")
                        understand = True
                    elif language_process.is_start_word(transcript.transcript):
                        talk("네 백색소음을 재생할게요")
                        queue_white_noise()
                        understand = True
                    else:
                        talk("이해하지 못했어요 다시 한번 말해주세요")
                elif language_process.is_led(transcript.transcript):
                    global led_on
                    global led_bright
                    if language_process.is_increase_word(transcript.transcript):
                        led_on = True
                        led_bright += 10
                        if led_bright > 100:
                            led_bright = 100
                        board_controll.change_led_bright(led_bright)
                        talk("네 LED 밝기를 높일게요")
                        understand = True
                    elif language_process.is_decrease_word(transcript.transcript):
                        led_on = True
                        led_bright -= 10
                        if led_bright < 0:
                            led_bright = 0
                        board_controll.change_led_bright(led_bright)
                        talk("네 LED 밝기를 줄일게요")
                        understand = True
                    elif language_process.is_stop_word(transcript.transcript):
                        led_on = False
                        board_controll.change_led_bright(0)
                        talk("네 LED를 끌게요")
                        understand = True
                    elif language_process.is_start_word(transcript.transcript):
                        led_on = True
                        board_controll.change_led_bright(100)
                        talk("네 LED를 켤게요")
                        understand = True
                    else:
                        talk("이해하지 못했어요 다시 한번 말해주세요")
                elif language_process.is_volume(transcript.transcript):
                    if language_process.is_increase_word(transcript.transcript):
                        if volume >= 1.00:
                            talk("현재 볼륨이 최대에요")
                        elif volume >= 0.80:
                            change_volume(1.00)
                            talk("네 볼륨을 최대로 키울게요")
                        else:
                            change_volume(volume+0.20)
                            talk("네 볼륨을 키울게요")
                        understand = True
                    elif language_process.is_decrease_word(transcript.transcript):
                        if volume <= 0.20:
                            talk("현재 볼륨이 최소에요")
                        elif volume <= 0.40:
                            change_volume(0.20)
                            talk("네 볼륨을 최소로 줄일게요")
                        else:
                            change_volume(volume-0.20)
                            talk("네 볼륨을 줄일게요")
                        understand = True
                    else:
                        talk("이해하지 못했어요 다시 한번 말해주세요")
                elif language_process.is_study_time_info(transcript.transcript):
                    data: dict = requesting.request_start_study_info()
                    talk("네 공부시간을 알려드릴게요")
                else:
                    talk("이해하지 못했어요 다시 한번 말해주세요")
        sequence = sequence_dict["IDLE"]
            # time.sleep(5)

listener = sr.Recognizer()
rn = sr.Recognizer()

main()
