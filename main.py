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
import os

from pynput import mouse


class EU4Popup(threading.Thread):
    text_lock = threading.Lock()
    noti_lock = threading.Lock()
    write_lock = threading.Lock()
    def __init__(self):
        self.p_x = 50
        self.p_y = 50
        self.r_x = 100
        self.r_y = 100
        threading.Thread.__init__(self)
        self.current_notification = dict()
        self.start()
   
    def speak(self, speak_text):
        with EU4Popup.write_lock:
            filename = "notification_sound.mp3"
            with open(filename, "w") as f:
                pass
            gtts.gTTS(speak_text, lang='en').save(filename)
            playsound(filename)
            try:
                os.remove(filename)
            except OSError as e:
                print("Error: ", e)

    def callback(self):
        self.window.quit()

    def sumbit_date(self, event):
    #Sanitize user entered string!
        try:
            datenoti_object = datetime.datetime.strptime(self.date_entry.get(), "%d.%m.%Y")
            date_foramted = datenoti_object.strftime("%d %B %Y")
            print(date_foramted)
        except:
            print(self.date_entry.get())
            print("Failed to add event")
            return

        if(datenoti_object in self.current_notification):
            print("Event allready exist, skipping")
            return
    
        notification = tk.Label(self.window, text=date_foramted + "\n I will do stuff")
        notification.pack()
        self.current_notification[datenoti_object] = notification
    
    def on_click(self, x,y, button, pressed):  
        if pressed:
            self.p_x = x
            self.p_y = y
            print("Pressed at ({},{})".format(self.p_x, self.p_y))
        else:
            self.r_x = x
            self.r_y = y
            print("Released at ({},{})".format(self.r_x, self.r_y))
            # Stop listener
            return False

    def new_boundary(self, parameter_list):
        print("New b coming up!")
        #To make sure the press button is not apart of the croping
        time.sleep(0.1)
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
    
    def run(self):
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.callback)
        self.display_text = tk.StringVar()
        self.eu4_date = tk.Label(self.window, textvariable=self.display_text)
        self.entry_text = tk.Label(self.window, text="Enter a date for notification:\nFormat: 01.11.1444")
        self.date_entry = tk.Entry(self.window)

        self.submit_button = tk.Button(self.window, text="Add Notification!")
        self.submit_button.bind("<Button-1>", self.sumbit_date)

        self.boundary_btn = tk.Button(self.window, text="Crop Date")
        self.boundary_btn.bind("<Button-1>", self.new_boundary)

        self.eu4_date.pack()
        self.boundary_btn.pack()
        self.entry_text.pack()
        self.date_entry.pack()
        self.submit_button.pack()

        self.window.mainloop()
    
    def set_text(self, text):
        with EU4Popup.text_lock:
            self.display_text.set(text)

    def update_notifications(self, curr_date_obj):
        with EU4Popup.noti_lock:
            delete_date = [date for date in self.current_notification if date <= curr_date_obj]
            for date in delete_date:
                self.current_notification[date].destroy()
                del self.current_notification[date]

                tts_thread = threading.Thread(target=self.speak, args=(date.strftime("%d %B %Y"), ))
                tts_thread.start()

                popup = tk.Toplevel()
                popup.wm_title("EU4 Notification")
                l = tk.Label(popup, text="Input")
                l.grid(row=0, column=0)
                b = ttk.Button(popup, text="Okay", command=popup.destroy)
                b.grid(row=1, column=0)

    def get_boundarybox(self):
        return {'top': self.p_y, 'left': self.p_x, 'width': abs(self.p_x-self.r_x), 'height': abs(self.p_y-self.r_y)}
if __name__ == "__main__":
    eu4 = EU4Popup()
    tick_time = time.time()
    sct = mss()
    text = "no date found"
    #TODO: Make the user set the box
    
    
    while eu4.is_alive():
        #TODO: Allow users to set timer on screenshot
        #Grab the screenshot
        curr_time = time.time()
        if(curr_time > tick_time):
            sct_img = sct.grab(eu4.get_boundarybox())
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
            cv2.imshow("Thresh",image)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break

        #Fancy GUI to display year
        try:
            curr_date_obj = datetime.datetime.strptime(text, "%d %B %Y")
            eu4.set_text(text)    
            eu4.update_notifications(curr_date_obj)
        except:           
            eu4.set_text("unknown date:" + text)


