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

sequence: int = 0

global sequence_dict

sequence_dict: dict = {
    "IDLE": 0,
    "WAKE_UP": 1,
    "LISTENING": 2,
    "SPEAKING": 3,
    "WAITING_NFC": 4
}

global white_noise_index

white_noise_index = 0

global white_noise_list

white_noise_list = [
    pygame.mixer.Sound("./audio/1.wav"),
    pygame.mixer.Sound("./audio/2.wav"),
    pygame.mixer.Sound("./audio/1.wav")
]

audio_dict: dict = {
    
    "네 공부 모드를 시작할까요?": "shall_we_start_study_mode.wav",
    "휴대폰을 올려 놓으셨군요 공부 모드를 시작합니다": "start_study_mode_with_phone.wav",
    "휴대폰을 올려 인식되지 않아 공부 모드가 종료되었어요": "phone_not_found_study_stop.wav",
    "네 공부모드를 시작할게요": "start_study_mode.wav",
    "네 공부모드를 종료할게요": "stop_study_mode.wav",
    "네 무었을 도와드릴까요?": "what_can_i_do.wav",
    "네 백색소음을 재생할게요": "play_white_noise.wav",
    "네 백색소음을 변경할게요": "change_white_noise.wav",
    "네 백색소음을 종료했어요": "stop_white_noise.wav",
    "네 볼륨을 줄일게요": "decrease_volume.wav",
    "네 볼륨을 키울게요": "increase_volume.wav",
    "현재 볼륨이 최대 입니다": "volume_max.wav",
    "현재 볼륨이 최소 입니다": "volume_min.wav",
    }

def waiting_for_idle() -> None:
    while sequence != 0:
        time.sleep(0.15)
    return

# SocketIO Connection Handeler

sio = socketio.AsyncClient()
sio.connect(os.environ['BACKEND_URL'])

@sio.on('nfc')
async def on_message(data):
    global sequence
    if sequence == sequence_dict["IDLE"]:
        sequence = sequence_dict["WAKE_UP"]
        talk('공부 모드를 시작 할까요?')
        transcript = take_command()
        await sio.emit('study', 'study start')
    elif sequence == sequence_dict["WAITING_NFC"]:
        sequence = sequence_dict["IDLE"]
        await sio.emit('study', 'study start')


@sio.on("led")
async def on_message(data):
    global sequence
    board_controll.change_led_bright(data)
    await waiting_for_idle()
    sequence = sequence_dict["WAKE_UP"]
    talk("LED 밝기를 조절했어요")
    sequence = sequence_dict["IDLE"]

@sio.on('volume')
async def on_message(data):
    change_volume(volume_val=data/100)

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
        time.sleep(0.1)
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




def take_command():
    with sr.Microphone() as source:
        rn.adjust_for_ambient_noise(source)
        print('listening...')
        voice = rn.listen(source)
        print('encoding...')
        base64_encoded_voice: str = base64.b64encode(voice.get_wav_data()).decode('utf-8')
        print('recognizing...')
        transcript: str = requesting.request_stt(base64_encoded_voice)
        return transcript
# def take_command() -> str: #for test
#     return requesting.return_value(input("명령을 입력하세요: "), False)

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
                        talk("네 공부모드를 시작할게요")
                        understand = True
                    elif language_process.is_stop_word(transcript.transcript):
                        talk("네 공부모드를 종료할게요")
                        understand = True
                    else:
                        talk("이해하지 못했어요 다시 말해주세요")
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
                        talk("이해하지 못했어요 다시 말해주세요")
                elif language_process.is_led(transcript.transcript):
                    if language_process.is_increase_word(transcript.transcript):
                        talk("네 LED 밝기를 키울게요")
                        understand = True
                    elif language_process.is_decrease_word(transcript.transcript):
                        talk("네 LED 밝기를 줄일게요")
                        understand = True
                    elif language_process.is_stop_word(transcript.transcript):
                        talk("네 LED를 끌게요")
                        understand = True
                    elif language_process.is_start_word(transcript.transcript):
                        talk("네 LED를 켤게요")
                        understand = True
                    else:
                        talk("이해하지 못했어요 다시 말해주세요")
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
                        talk("이해하지 못했어요 다시 말해주세요")
                else:
                    talk("이해하지 못했어요 다시 말해주세요")
            sequence = sequence_dict["IDLE"]

listener = sr.Recognizer()
rn = sr.Recognizer()

main()
