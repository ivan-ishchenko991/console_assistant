import pyowm
from commands_t9 import commands_for_weather
from prompt_toolkit import prompt



owm = pyowm.OWM('fb7b8f2b668627b6f83f604ee25f41a3')

def weather():
    try:
        while True:
            place = prompt("Write your city: ", completer=commands_for_weather)
            if place in r'exit|close|good bye':
                print("Good bye!")
                break

            mrg = owm.weather_manager()

            observation = mrg.weather_at_place(place)
            w = observation.weather
            t = w.temperature('celsius')['temp']
            print("In " + place + " " + w.detailed_status + " now." +
                "\nTemperature: " + str(round(t)) + "\u00b0" + "." +
                "\nHumidity is " + str(w.humidity) + "%." +
                "\nWind speed is " + str(w.wind()['speed']) + " meters per second.")
    except(pyowm.commons.exceptions.NotFoundError):
        print("Please, write the correct city name.")
        