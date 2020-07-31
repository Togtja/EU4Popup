import numpy as np
import cv2
import pytesseract
import time
import gtts

import tkinter as tk
from tkinter import ttk

import datetime

from mss import mss
from PIL import Image
from screeninfo import get_monitors

from playsound import playsound

import threading

def speak(speak_text):
    f = open("notification_sound.mp3", "w")
    f.close()
    gtts.gTTS(speak_text, lang='en').save(f.name)
    playsound(f.name)
    
current_notification = dict()

#TODO: Make the user set the box
bounding_box = {'top': 13, 'left': get_monitors()[0].width - 220, 'width': 120, 'height': 25}

sct = mss()
window = tk.Tk()
display_text = tk.StringVar()
eu4_date = tk.Label(window, textvariable=display_text)
entry_text = tk.Label(window, text="Enter a date for notification:\nFormat: 01.11.1444")
date_entry = tk.Entry(window)

def sumbit_date(event):
    #Sanitize user entered string!
    try:
        datenoti_object = datetime.datetime.strptime(date_entry.get(), "%d.%m.%Y")
        date_foramted = datenoti_object.strftime("%d %B %Y")
        print(date_foramted)
    except:
        print("Failed to add event")
        return
    
    notification = tk.Label(window, text=date_foramted + "\n I will do stuff")
    notification.pack()
    current_notification[datenoti_object] = notification

submit_button = tk.Button(window, text="Add Notification!")
submit_button.bind("<Button-1>", sumbit_date)


eu4_date.pack()
entry_text.pack()
date_entry.pack()
submit_button.pack()
tick_time = time.time()
text = "no date found"

if __name__ == "__main__":

    while True:
        #TODO: Set timer on screenshot
        #Grab the screenshot
        curr_time = time.time()
        if(curr_time > tick_time):
            sct_img = sct.grab(bounding_box)
            #Translate it to an np array
            image = np.array(sct_img)
            #Use fancy openCV image processing to clean out the photo
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
            thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            tick_time = time.time() + 0.2
            #Try to grab the text from the photo
            #TODO: Do text sanitizing so we can easier compare
            text = pytesseract.image_to_string(thresh)

        #Fancy GUI to display year
        try:
            curr_date_obj = datetime.datetime.strptime(text, "%d %B %Y")
            display_text.set(text)
        except:
            display_text.set("unknown date:" + text)

        delete_date = [date for date in current_notification if date <= curr_date_obj]
        for date in delete_date:
            current_notification[date].destroy()
            del current_notification[date]
            tts_thread = threading.Thread(target=speak, args=(date.strftime("%d %B %Y"), ))
            tts_thread.start()

            popup = tk.Toplevel()
            popup.wm_title("EU4 Notification")
            l = tk.Label(popup, text="Input")
            l.grid(row=0, column=0)

            b = ttk.Button(popup, text="Okay", command=popup.destroy)
            b.grid(row=1, column=0)

        window.update_idletasks()
        window.update()


