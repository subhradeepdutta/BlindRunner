#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr

# Record Audio
r = sr.Recognizer()
r.energy_threshold = 3700
 
# Speech recognition using Google Speech Recognition
try:
    with sr.Microphone() as source:
        print("Adjusting ambient noise levels! Please wait")
        r.adjust_for_ambient_noise(source, duration=1);
        print("Speak now!")
        audio = r.listen(source, timeout=1.5)
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    speech_to_text_output = r.recognize_google(audio, language="en-IN")
    print("You said: " + speech_to_text_output)

except sr.WaitTimeoutError as e:
    print("Timeout; {0}".format(e))

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")

except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

#Check if text has valid keyword or not
try:
    if "left" in speech_to_text_output:
        command = "left"
    elif "right" in speech_to_text_output:
        command = "right"
    elif "front" in speech_to_text_output:
        command = "front"
    elif "back" in speech_to_text_output:
        command = "back"
    elif "stop" in speech_to_text_output:
        command = "stop"
    print("Identified the command as  ---->  " + command)
    print("Transmitting to AWS Server")

except NameError:
    print("Did not recognize a valid command")
    print("Terminating operation")
