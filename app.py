from dotenv import load_dotenv
load_dotenv()

from time import time
import speech_recognition as sr
import datetime, base64, time, socketio, os

from module import requesting, language_process, board_controll
from playsound import playsound

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

audio_dict: dict = {
    "공부모드를 시작할게요": "start_study_mode.mp3",
    "네 공부 모드를 시작할까요?": "shall_we_start_study_mode.mp3",
    "휴대폰을 올려 놓으셨군요 공부 모드를 시작할까요?": "shall_we_start_study_mode_with_phone.mp3",
    "휴대폰을 올려 놓으시지 않아 공부 모드가 종료됩니다": "phone_not_found_study_stop.mp3",
    "네 공부 모드를 종료할게요": "stop_study_mode.mp3",
    "네 무었을 도와드릴까요?": "what_can_i_do.mp3",
    "네 백색소음을 재생할게요": "play_white_noise.mp3",
    "네 백색소음을 변경할게요": "change_white_noise.mp3",
    "네 백색소음을 종료할게요": "stop_white_noise.mp3",
    "네 볼륨을 줄일게요": "decrease_volume.mp3",
    "네 볼륨을 키울게요": "increase_volume.mp3",
    "현재 볼륨이 최대 입니다": "volume_max.mp3",
    "현재 볼륨이 최소 입니다": "volume_min.mp3"
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


def talk(text) -> None:
    global sequence
    ex_sequence: int = sequence
    sequence = sequence_dict["SPEAKING"]
    print(text)
    playsound("audio/" + audio_dict[text])
    sequence = ex_sequence


def take_command() -> str:
    with sr.Microphone() as source:
        rn.adjust_for_ambient_noise(source)
        print('listening...')
        voice = rn.listen(source)
        base64_encoded_voice: str = base64.b64encode(voice.get_wav_data()).decode('utf-8')
        transcript: str = requesting.request_stt(base64_encoded_voice)
        return transcript

def main() -> None:
    global sequence
    while True:
        transcript: requesting.return_value = take_command()
        if not transcript.err:
            talk("대화를 처리하는 과정에서 문제가 발생했습니다")
            continue
        if language_process.is_wake_up_word(transcript.transcript):
            waiting_for_idle()
            print(sequence)
            sequence = sequence_dict["WAKE_UP"]
            talk('네 무었을 도와드릴까요?')
            sequence = sequence_dict["LISTENING"]
            transcript: requesting.return_value = take_command()
            if not transcript.err:
                talk("대화를 처리하는 과정에서 문제가 발생했습니다")
                sequence = sequence_dict["IDLE"]
                continue
            if language_process.is_study_mode(transcript.transcript):
                understand = False
                while not understand:
                    if language_process.is_start_word(transcript.transcript):
                        talk("네 공부모드를 시작할게요")
                        understand = True
                    elif language_process.is_stop_word(transcript.transcript):
                        talk("네 공부모드를 종료할게요")
                        understand = True
                    else:
                        talk("이해하지 못했어요 다시 말해주세요")
            elif language_process.is_white_noise(transcript.transcript):
                understand = False
                while not understand:
                    if language_process.is_play_word(transcript.transcript):
                        talk("네 백색소음을 재생할게요")
                        understand = True
                    elif language_process.is_change_word(transcript.transcript):
                        talk("네 백색소음을 변경할게요")
                        understand = True

listener = sr.Recognizer()
rn = sr.Recognizer()

main()
