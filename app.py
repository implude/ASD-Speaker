from dotenv import load_dotenv
load_dotenv()

from time import time
import speech_recognition as sr
import datetime, base64, time, socketio, os

from module import requesting, language_process, board_controll

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
    sequence = ex_sequence



def take_command() -> str:
    with sr.Microphone() as source:
        rn.adjust_for_ambient_noise(source)
        print('listening...')
        voice = rn.listen(source)
        with open("microphone-results.wav", "wb") as f:
            f.write(voice.get_wav_data())
        base64_encoded_voice: str = base64.b64encode(voice.get_wav_data()).decode('utf-8')
        transcript: str = requesting.request_stt(base64_encoded_voice)
        return transcript

def main() -> None:
    global sequence
    while True:
        transcript: requesting.return_value = take_command()
        if transcript.err:
            talk("대화를 처리하는 과정에서 문제가 발생했습니다")
        if language_process.is_wake_up_word(transcript.transcript):
            waiting_for_idle()
            print(sequence)
            sequence = sequence_dict["WAKE_UP"]
            talk('네 무었을 도와드릴까요?')
            sequence = sequence_dict["LISTENING"]



listener = sr.Recognizer()
rn = sr.Recognizer()

main()
