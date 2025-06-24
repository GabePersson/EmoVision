import speech_recognition as sr
import json


def listen_user_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something")
        try:
            audio = r.listen(source, phrase_time_limit=10)
            speek_content = json.loads(r.recognize_vosk(audio, language='zh-CN'))
            speek_content = speek_content["text"].replace(" ", "")
            return speek_content
        except Exception as e:
            raise e


def restore_voice_symbol(text: str):
    result = text
    return result


def voice_input():
    text = listen_user_voice()
    if text == "":
        return ""
    text = restore_voice_symbol(text)
    return text

if __name__ == '__main__':
    print(voice_input())
