import speech_recognition as sr
import json


def listen_user_voice(data_path):
    r = sr.Recognizer()
    with sr.AudioFile(data_path) as source:
        try:
            audio = r.listen(source, phrase_time_limit=10)
            speek_content = json.loads(r.recognize_vosk(audio, language='zh-CN'))
            speek_content = speek_content["text"].replace(" ", "")
            return speek_content
        except Exception as e:
            raise e


def restore_voice_symbol(text: str):
    #TODO:最好搞个模型恢复一下符号，paddlespeech只能在3.7中使用，但是SpeechRecognition只能在3.10中用
    result = text
    return result


def voice_input(data_path):
    text = listen_user_voice(data_path)
    if text == "":
        return ""
    text = restore_voice_symbol(text)
    return text

if __name__ == '__main__':
    print(voice_input('../data/tempaudio~1.wav'))
