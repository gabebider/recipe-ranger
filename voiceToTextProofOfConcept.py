import speech_recognition as sr
import pyttsx3

# pip install SpeechRecognition
# pip install pyaudio
# had to brew install portaudio
# pip install pyttsx3

def listener():
    # create a recognizer object
    r = sr.Recognizer()

    # use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        recongized = r.recognize_google(audio, show_all=True)
        text = recongized['alternative'][0]['transcript']
        confidence_score = recongized['alternative'][0]['confidence']
        return text, confidence_score
    except sr.UnknownValueError:
        # print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        # print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def reader():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text, confidence_score = listener()
    if text is not None:
        print(text)
        print(f"confidence_score: {confidence_score}")
        reader()
