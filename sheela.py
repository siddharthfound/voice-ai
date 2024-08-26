import speech_recognition as sr
import pyttsx3
import openai

# Set your OpenAI API  
openai.api_key = 'xxxxx'

def recognize_speech(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError: 
        return "I could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def process_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    while True:
        print("Listening...")
        text = recognize_speech(recognizer, microphone)
        print(f"You said: {text}")
        response = process_text(text)
        print(f"Response: {response}")
        speak(response)
