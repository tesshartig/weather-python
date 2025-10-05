from tkinter import *
import ttkbootstrap as ttk
import requests
from PIL import ImageTk, Image
from io import BytesIO
import tkintermapview
from datetime import datetime

#aby to fungovalo v add city but
buttons = [ ]



def get_city():
    city = entry_city.get()
    entry_city.delete(0, END)


    #API
    api_key = "cbbfdb52c56efc44e3bc736fb212f9e0"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    def destroy_error():
        error_label.destroy()
        destroy_error.destroy()

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        city_name = data["name"]
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        latitude = data["coord"]["lat"]
        longtitude = data["coord"]["lon"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        pressure = data["main"]["pressure"]
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]



        weather_info = {
            "city":city_name,
            "temp":temperature,
            "description":weather_description,
            "humidity":humidity,
            "wind":wind_speed,
            "latitude":latitude,
            "longtitude":longtitude,
            "temp_min":temp_min,
            "temp_max":temp_max,
            "pressure":pressure,
            "sunrise":sunrise,
            "sunset":sunset


        }
        
        #RECTANGLES - MAIN WINDOW
        def add_city_but(city_name):
            global buttons
            max_rows_per_column = 5

            for  btn in buttons:
                if btn["text"].lower() == city_name.lower():
                    return

            index = len(buttons)
            row = index % max_rows_per_column
            col = index // max_rows_per_column
            
            x_pos = 0.1 + col * 0.3
            y_pos = 0.3 + row * 0.1

            city_but = Button(main_window,text=city_name, font=("Times New Roman", 20), foreground="white", background="black", command=lambda:create_weather_screen(weather_info))
            city_but.place(relx=x_pos, rely=y_pos)
            buttons.append(city_but)

        add_city_but(city_name)
        #print(weather_info)


        def create_weather_screen(weather_info):
            global app_width, app_height
            weather_screen = Toplevel(main_window)
            weather_screen.minsize(800, 600)
            weather_screen.resizable(False, False)
            #try:
                #weather_screen.iconbitmap("weather.ico")
            #except:
                #pass

            x = (screen_width / 2) - (app_width / 2)
            y = (screen_height / 2) - (app_height/2)

            weather_screen.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

            #POZADÍ
            description = weather_info["description"].lower()
            if "rain" in description:
                background = "rain.jpg"
            elif "cloud" in description:
                background = "cloudy.jpg"
            elif "clear" in description:
                background = "sunny_upd.png"
            elif "snow" in description:
                background = "snowy.jpg"
            elif "clear sky" in description:
                background="clear_sky.jpg"
            else:
                background = "neutral.png"

            img = Image.open(background)
            img = img.resize((800,600), Image.Resampling.LANCZOS)
            background = ImageTk.PhotoImage(img)
            weather_screen.background = background

            canvas_bg_weather = Canvas(weather_screen, width=800, height=600)
            canvas_bg_weather.pack(fill="both", expand=True)
            canvas_bg_weather.create_image(0,0, image=background, anchor="nw")

            #MAPA
            lat = weather_info["latitude"]
            lon = weather_info["longtitude"]

            map_widget = tkintermapview.TkinterMapView(weather_screen, width=310, height=170)
            map_widget.place(x=50, y=130)

            map_widget.set_position(latitude, longtitude)
            map_widget.set_zoom(12.5)

            #SOUŘADNICE POD MAPOU¨
            coordinates_label = Label(weather_screen, text=f"{latitude} {longtitude}")
            coordinates_label.place(x=50, y=300)


            #INICIALIZACE POZADÍ
            canvas_bg_weather.image = background

            
            #STYLE
            style = ttk.Style()
            style.configure("Custom.TLabel", 
                font=("Arial", 20, "bold"), 
                foreground="black", 
                background="white", 
                padding=10)
            #CITY LABEL
            if len(city_name)> 8:
                font_size = 30
            else:
                font_size = 50
            city_label = ttk.Label(weather_screen, text=city_name,font=("Times New Roman", font_size), style="Custom.TLabel")
            city_label.place(relx=0.06, rely=0.04)

            #TEPLOTA V ROHU
            temp_label = Label(weather_screen, text=f"{temperature}°C", font=("Times New Roman", 25))
            temp_label.place(relx=0.80, rely=0.075)

            #TEPLOTA OVÁL!!!!¨
            temp_min_label = Label(weather_screen, text=temp_min, font=("Times New Roman", 25), foreground="pink", cursor="circle")
            temp_min_label.place(relx=0.05, rely=0.75)

            temp_max_label = Label(weather_screen, text=temp_max, font=("Times New Roman", 25), foreground="pink")
            temp_max_label.place(relx=0.35, rely=0.75)

            now_label=Label(weather_screen, text="Now", font=("Times New Roman", 45))
            now_label.place(relx=0.175, rely=0.65)

            #DRUHÁ ŘADA
                #DESCRIPTION
            description_label = Label(weather_screen, text=description, font=("Times New Roman", 25))
            description_label.place(relx=0.55 ,rely=0.25)

            #tlak
            pressure_label = Label(weather_screen, text=f"pressure:{pressure} hPa", font=("Times New Roman", 25))
            pressure_label.place(relx=0.55, rely=0.35)

            #wind_speed
            wind_speed_label = Label(weather_screen, text=f"wind speed:{wind_speed} m/s", font=("Times New Roman", 25))
            wind_speed_label.place(relx=0.55, rely=0.45)

            #SUNSET A SUNRISE PŘEVOD ATD
            sunrise_time = datetime.fromtimestamp(sunrise).strftime("%H:%M")
            sunset_time = datetime.fromtimestamp(sunset).strftime("%H:%M")

            sunrise_label = Label(weather_screen, text=sunrise_time, font=("Times New Roman", 30))
            sunrise_label.place(relx=0.56, rely=0.77)

            sunset_label = Label(weather_screen, text=sunset_time, font=("Times New Roman", 30))
            sunset_label.place(relx=0.82, rely=0.77)


                


        #VOLÁNÍ FUNKCE
        create_weather_screen(weather_info)



    else:
        error_label = Label(text="City not found", font=("Times New Roman", 20))
        error_label.place(relx=0.5, rely=0.5, anchor="center")

        destroy_error = Button(text="X", font=("Times New Roman", 15), command=destroy_error)
        destroy_error.place(relx=0.65, rely=0.5, anchor="center")

    

    

def weather_label():
    pass

def enter_add(event):
    get_city()
    entry_city.delete(0, END)


app_width = 800
app_height = 600

main_window = Tk()
main_window.minsize(app_width, app_height)
main_window.title("Weather app")
main_window.resizable(False, False)
#try:
    #main_window.iconbitmap("weather.ico")
#except:
    #pass

#zjistit rozměry od uživatele
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height/2)

main_window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

#pozadí
background = PhotoImage(file = "sky_upd.png")

canvas_bg = Canvas(main_window, width=app_width, height=app_height)
canvas_bg.pack()

canvas_bg.create_image(0, 0, image = background, anchor="nw")

#ENTRY - TTK
entry_city = ttk.Entry(main_window, font=("Times New Roman", 25), cursor="xterm")
entry_city.place(x=275, y=75, width=210, height=50)

entry_city.bind("<Return>", enter_add)
#ADD BUTTON - TTK

add_but = ttk.Button(main_window, text="Add", width=20, padding=(10, 15), style = "style_but", command=get_city)
add_but.place(x=500, y = 75)

#Label
#weather_label = Label(text="Weather app", font=("Times New Roman", 25))
#weather_label.place(x=50, y=75)



mainloop()