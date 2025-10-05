from tkinter import *
import ttkbootstrap
import requests
from PIL import Image, ImageTk


def get_weather(event=None):
    global api_key, url, city_id, response

    city_id = city_entry.get()
    #API
    api_key = "cbbfdb52c56efc44e3bc736fb212f9e0" 
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_id}&appid={api_key}&units=metric&lang=cz"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]

        
    
        weather_rect = create_rounded_rect()
        weather_label = (text=data["weather"][0]["description"])


    print(response.json())

def weather_label():
    pass

def create_rounded_rect(canvas, x1, y1, x2, y2, r=25, **kwargs):
    """
    Vykreslí zaoblený obdélník na Canvas.
    x1, y1, x2, y2 - souřadnice rohu obdélníku
    r - poloměr rohů
    kwargs - další argumenty jako fill=, outline= atd.
    """
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

app_width = 800
app_height = 600
#window
window = Tk()
window.minsize(800 , 600)
window.resizable(False, False)
window.title("Weather")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height/2)

window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

#background
background = PhotoImage(file="sky.png")

canvas_bg = Canvas(window, width=app_width, height=app_height)
canvas_bg.pack()

canvas_bg.create_image(0, 0, image=background, anchor="nw")

#entry
city_entry = ttkbootstrap.Entry(window, width=25, background="#b3e9eb", font=("Times New Roman", 25, "italic"), justify="center")
city_entry.place(x=200, y=75)

city_entry.bind("<Return>", get_weather)


#ok_button
ok_button = Button(text="ok.", font=("Times New Roman", 25, "bold"), command=get_weather)
ok_button.place(x=300,y=75)


window.mainloop()