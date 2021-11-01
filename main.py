import requests
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
from configparser import ConfigParser
import time


# The url link will be cast to a variable named 'url'
url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

# Stores the api key id
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


# Creates the instance of the clock function to display time
def clock():
    hours = time.strftime('%H')
    minutes = time.strftime('%M')
    seconds = time.strftime('%S')
    am_pm = time.strftime('%p')
    day = time.strftime('%A')
    time_zone = time.strftime('%Z')

    clock_l.config(text=hours + ':' + minutes + ':' + seconds + " " + am_pm)
    clock_l.after(1000, clock)

    clock_l_2.config(text=time_zone + ", " + day)


# The rest api grabs the weather data
def get_weather(city):

    # The api GET Request will call the url
    request = requests.get(url.format(city, api_key))

    # Json will retrieve the data
    data = request.json()

    # If request is true
    if request:

        # The weather data is then stored in key-value pairs, which can be accessed later
        city = data['name']
        country = data['sys']['country']
        weather = data['weather'][0]['main']
        humidity = data['main']['humidity']
        temp_kelvin = data['main']['temp']
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        pressure = data['main']['pressure']
        final = (city, country,  weather, int(temp_fahrenheit),  humidity, pressure)
        return final

    # If the location is false, it returns None
    else:
        return None


# Dynamically updates the weather depending on location
def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        print(weather)
        location_lbl['text'] = f'{weather[0]}, {weather[1]}'
        temperature_label['text'] = "{:.2f}°F".format(weather[3])
        weather_l['text'] = weather[2]
        humidity_label['text'] = f"Humidity: {weather[4]}"
        pressure_label['text'] = f"Pressure: {weather[5]}"
    else:
        # Error message is displayed if city input is wrong
        messagebox.showerror('Error', f'Can not find city {city}')


# Starts the foreground off the application
weather_screen = tk.Tk()
weather_screen.geometry('700x450')
weather_screen.title('Weather Application')

# Sets the background image in the GUI
image = PhotoImage(file="Beautiful Clouds.png")
background_image = Label(weather_screen, image=image)
background_image.place(x=0, y=0, relwidth=1, relheight=1)

# Converting the png file into an ico/icon
ico = Image.open('Beautiful Clouds.png')
photo = ImageTk.PhotoImage(ico)
weather_screen.wm_iconphoto(False, photo)

# Add labels, buttons and text
city_text = StringVar()
city_entry = Entry(weather_screen, textvariable=city_text)
city_entry.pack()

Search_btn = Button(weather_screen, text="Search weather", width=20, command=search, bg='silver')
Search_btn.pack()

location_lbl = Label(weather_screen, text="", font={'bold', 20}, width=15, bg='dark red')
location_lbl.pack()

temperature_label = Label(weather_screen, text="", font={'bold', 20}, width=15, bg='light blue')
temperature_label.pack()

humidity_label = Label(weather_screen, text="", font={'bold', 20}, width=15, bg='green')
humidity_label.pack()

pressure_label = Label(weather_screen, text="", font={'bold', 20},  width=15, bg='pink')
pressure_label.pack()

weather_l = Label(weather_screen, text="", font={'bold', 20},  width=15, bg='purple')
weather_l.pack()

clock_l = Label(weather_screen, text="", font=("Helvetica", 40), fg='green', bg='black')
clock_l.pack(pady=20)

clock_l_2 = Label(weather_screen, text="", font=("Helvetica", 14))
clock_l_2.pack()

# Displays the time, day, and time zone
clock()

weather_screen.mainloop()


