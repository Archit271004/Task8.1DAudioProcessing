import speech_recognition as sr
from gpiozero import LED
from gpiozero.pins.rpigpio import RPiGPIOFactory
from time import sleep

# Setup GPIO factory explicitly for controlling pins
pin_factory = RPiGPIOFactory()
led = LED(17, pin_factory=pin_factory)

speech_recognizer = sr.Recognizer()

def recognize_commands(audio_path):
    with sr.AudioFile(audio_path) as source:
        audio_data = speech_recognizer.record(source)
        try:
            detected_command = speech_recognizer.recognize_sphinx(audio_data)
            print(f"Detected command: {detected_command}")
            return detected_command
        except sr.UnknownValueError:
            print("Unable to understand the audio")
            return ""
        except sr.RequestError as error:
            print(f"Error in request: {error}")
            return ""

def manage_led(command):
    if "on" in command.lower():
        led.on()
        print("LED turned on")
    elif "off" in command.lower():
        led.off()
        print("LED turned off")

audio_path = "/home/archit27/Music/record_out.wav"

try:
    while True:
        command = recognize_commands(audio_path)
        manage_led(command)
        sleep(10)
except KeyboardInterrupt:
    print("Program terminated by user")
    led.off()
