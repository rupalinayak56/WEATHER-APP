import tkinter as tk
from PIL import Image,ImageTk
import requests
from tkinter import ttk # import for combobox
import threading  # For threading to fetch data


root=tk.Tk() #creates window
root.title('Weather App') # giving title for window
root.geometry('700x500')
img=Image.open('./bg1.jpg')
img=img.resize((700,530),Image.LANCZOS)
img_photo=ImageTk.PhotoImage(img)

bg_lbl=tk.Label(root,image=img_photo)
bg_lbl.place(x=0,y=0,width=700,height=530)

heading_ttl=tk.Label(bg_lbl,text='Earth Including Over 200,000 Cities!  ',fg='goldenrod',bg='teal',font=('Arial',20,'bold'))
heading_ttl.place(x=100,y=20)

frame_one=tk.Frame(bg_lbl,bg='white',bd=5)
frame_one.place(x=100,y=70,width=490,height=47)

txt_box=tk.Entry(frame_one,fg='darkslategrey',font=('Arial',12,'bold'),width=30)
txt_box.grid(row=0,column=0,sticky='W')

# combobox for temperature unit
unit_var = tk.StringVar(value='imperial')  # Default to Fahrenheit
unit_combo = ttk.Combobox(frame_one, textvariable=unit_var, values=['imperial', 'metric'], state='readonly', width=10)
unit_combo.grid(row=0, column=1, padx=5)
unit_combo.current(0)  # Set default selection

btn = tk.Button(frame_one, text='Get Weather', bg='teal', fg='goldenrod', font=('Arial', 12, 'bold'), command=lambda: get_weather(txt_box.get()))
btn.grid(row=0,column=2,padx=5)

frame_two=tk.Frame(bg_lbl,bg='goldenrod',bd=5)
frame_two.place(x=100,y=130,width=490,height=350)

result=tk.Label(frame_two,font=30,bg='white',justify='left',anchor='nw')
result.place(relwidth=1,relheight=1)

weather_icon=tk.Canvas(result,bg='white',bd=0,highlightthickness=0)
weather_icon.place(relx=.75,rely=0,relwidth=1,relheight=0.5)

loading_label = tk.Label(frame_two, text='Loading...', bg='white', font=('Arial', 14), fg='teal')
loading_label.place(relx=0.5, rely=0.5, anchor='center')
loading_label.pack_forget()

# key: 92bd1469f771f2f2ff3d124abfb7664d
# api url: https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

def format_response(weather):
    try:

        city = (weather['name'])
        condition = (weather['weather'][0]['description'])
        temp = (weather['main']['temp'])
        unit = '°F' if unit_var.get() == 'imperial' else '°C'
        windspeed= (weather['wind']['speed'])
        humidity= (weather['main']['humidity'])
        country= (weather['sys']['country'])
        final_str = f"City: {city}\nCondition: {condition}\nTemperature: {temp}{unit}\nWind Speed:{windspeed}mph\nHumidity:{humidity}%\nCountry:{country}"
    except:
        final_str='There was a problem retrieving information'
    return final_str


def get_weather(city):
    loading_label.pack()  # Show loading message
    btn.config(state='disabled')  # Disable button during fetch
    weather_key='92bd1469f771f2f2ff3d124abfb7664d'
    url='https://api.openweathermap.org/data/2.5/weather'
    params={'appid':weather_key,'q':city , 'units':unit_var.get()}
    response=requests.get(url,params)
    print(response.json())
    if response.status_code==200:

        weather=response.json()
        result['text']=format_response(weather)

        icon_name=weather['weather'][0]['icon']
        open_image(icon_name)
    else:
        result['text'] = 'City not found. Please check your input.'

    loading_label.pack_forget()  # Hide loading message
    btn.config(state='normal') # enable button again

def open_image(icon):
    size = int(frame_two.winfo_height() * 0.25)
    img = Image.open(f'./img/{icon}.png').resize((size, size), Image.LANCZOS)
    img_photo = ImageTk.PhotoImage(img)

    weather_icon.delete('all')
    weather_icon.create_image(0, 0, anchor='nw', image=img_photo)
    weather_icon.image = img_photo

root.mainloop()