#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr

#IBM_USERNAME = "fe63dfe9-92e5-4c7b-8dc6-e84458c33f79"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
#IBM_PASSWORD = "L4QpXxfTTeol"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
 
# Record Audio
r = sr.Recognizer()
r.energy_threshold = 500
with sr.Microphone() as source:
    print("Adjusting ambient noise levels!")
    r.adjust_for_ambient_noise(source, duration = 1);
    print("Speak now!")
    audio = r.listen(source, timeout=1)
 
# Speech recognition using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("You said: " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
