import speech_recognition as sr
# import pyttsx3
# import pywhatkit
import datetime, base64

from dotenv import load_dotenv

load_dotenv()

from module import requesting, language_process

from gtts import gTTS

eng_wav = gTTS('Hello World!') 
eng_wav.save('eng.wav')

listener = sr.Recognizer()
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)
rn = sr.Recognizer()


def talk(text):
    print(text)
#     engine.say(text)
#     engine.runAndWait()


def take_command():

    with sr.Microphone() as source:
        rn.adjust_for_ambient_noise(source)
        print('listening...')
        voice = rn.listen(source)
        base64_encoded_voice: bytes = base64.b64encode(voice.get_wav_data())
        transcript: str = requesting.request_stt(base64_encoded_voice)
        return transcript


def main():
    while True:
        transcript: str = take_command()
        if language_process.is_wake_up_word(transcript):
            talk('안녕하세요 세리입니다.')

main()
