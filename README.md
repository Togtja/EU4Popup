# EU4Popup

## What is it

EU4Popup allows you to set a date, and get a popup when that date has been reach.
It is useful for time based event and button you can only click every x years. Such as the estate button. It can also be used to give you reminder when you are supposed to do certain things, such as when truce ends.

Currently it will TTS you the date and send you a popup. the only reason it currently TTS you is because the popup is very hard to notice

## Usage

To install and use. you need to install all the external python libraries, my goal is to create a executable, but that is currently on my TODO.

## How it works

Simply put it grabs a screenshot of EU4's date and read that date as text, and compare to other dates.

## Todo

* Allow users to set where to capture the screenshot of the date [In Progress]
* Allow for configurations, such as: Timer on screenshot, Toggle TTS
* Sanitize text to allow for better accuracy
* Save user notifications
* Add a error logger to the UI
* Add Ability to remove notifications
* ~~Add preview of cropping/image capture~~[Finished]

## External Libs

I use a bunch of external libs, I hope to cut down on some of them

### OpenCv

Used for image processing. [GitHub](https://github.com/skvark/opencv-python), [PyPi](https://pypi.org/project/opencv-python/)

### Pytesseract

Used to read text of image. [GitHub](https://github.com/madmaze/pytesseract), [PyPi](https://pypi.org/project/pytesseract/)

### gTTS

API of Google translate and TTS. [GitHub](https://github.com/pndurette/gTTS), [PyPi](https://pypi.org/project/gTTS/)

### MSS

Really fast library to grab screenshots. [GitHub](https://github.com/BoboTiG/python-mss), [PyPi](https://pypi.org/project/mss/)

### playsound

A cross-platform way to play the sounds I get from gTTS. [GitHub](https://github.com/TaylorSMarks/playsound), [PyPi](https://pypi.org/project/playsound/)

### pynput

A cross-platform library to handle input devices, in my case, I handle som mouse clicks. [GitHub](https://github.com/moses-palmer/pynput), [PyPi](https://pypi.org/project/pynput/)