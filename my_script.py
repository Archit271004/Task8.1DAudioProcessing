mport speech_recognition as sr
from gpiozero import LED
from gpiozero.pins.rpigpio import RPiGPIOFactory
from time import sleep

# Use RPiGPIOFactory explicitly
factory = RPiGPIOFactory()
led = LED(17, pin_factory=factory)

recognizer = sr.Recognizer()

def listen_for_commands(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            command = recognizer.recognize_sphinx(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand?")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

def control_led(command):
    if "on" in command.lower():
        led.on()
        print("LED is on")
    elif "off" in command.lower():
        led.off()
        print("LED is off")

audio_file = "/home/archit27/Music/record_out.wav"

try:
    while True:
        command = listen_for_commands(audio_file)
        control_led(command)
        sleep(10) 
except KeyboardInterrupt:
    print("Program stopped manually")
    led.off()
