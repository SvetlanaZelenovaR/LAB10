import speech_recognition as sr
import pyttsx3
import webbrowser
import requests


def speak(what):
    print(what)
    tts.say(what)
    tts.runAndWait()
    tts.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="en-EN").lower()
        print('You said: ' + voice)
        if voice.split(' ')[0] in commands:
            execute_cmd(voice)
        else:
            print('')

    except sr.UnknownValueError:
        print('Sorry, I did not understand. Try again')
    except sr.RequestError as e:
        print('Please, check your internet connection')


def execute_cmd(cmd):
    response_word = requests.get(url + cmd.split(' ')[1])
    resp = response_word.json()

    if 'find' in cmd:
        speak("Here's information about your word")
        webbrowser.get().open(url + cmd.split(' ')[1])

    if 'save' in cmd:
        data = open('saved_meaning', 'w')
        data.write(resp[0]['meanings'][0]['definitions'][0]['definition'])

    if 'meaning' in cmd:
        speak(resp[0]['meanings'][0]['definitions'][0]['definition'])

    if 'link' in cmd:
        webbrowser.get().open(resp[0]["sourceUrls"][0])

    if 'example' in cmd:
        examples = []
        for i in range(len(resp)):
            for j in range(len(resp[i]['meanings'][0]['definitions'])):
                if 'example' in resp[i]['meanings'][0]['definitions'][j]:
                    examples.append(resp[i]['meanings'][0]['definitions'][j]['example'])
        if len(examples) != 0:
            speak(examples[0])
        else:
            speak("Sorry, there's no examples")


commands = ['find', 'save', 'meaning', 'link', 'example']
url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voice', voices[1].id)

speak("Hello, I'm listening for you!")

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

while True:
    with m as source:
        audio = r.listen(source)
    callback(r, audio)



