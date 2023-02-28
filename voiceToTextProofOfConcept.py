import speech_recognition as sr
import pyttsx3

# pip install SpeechRecognition
# pip install pyaudio
# had to brew install portaudio
# pip install pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# create a recognizer object
r = sr.Recognizer()

# use the default microphone as the audio source
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    text = r.recognize_google(audio, show_all=True)
    text = text['alternative'][0]['transcript']
    print("You said: " + text)
    engine.say(text)
    engine.runAndWait()
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
