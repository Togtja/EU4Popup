# EU4Popup
## What is it?
EU4Popup allows you to set a date, and get a popup when that date has been reach.
It is usefull for time based event and button you can only click every x years. Such as the estate button. It can also be used to give you reminder when you are supposed to do certain things, such as when truce ends.

Currently it will TTS you the date and send you a popup. the only reason it currently TTS you is becuase the popup is very hard to notice
## Usage
To install and use. you need to install all the external python libaries, my goal is to create a executable, but that is currently on my TODO

## How it works
Simply put it grabs a screenshot of EU4's date and read that date as text, and compare to other dates.

## Todos
* Allow users to set where to capture the screenshot of the date
* Allow for configurations, such as: Timer on scrrenshot, Toggle TTS
* Sanitize text to allow for better accuracy

# External Libs
I use a bunch of external libs, I hope to cut down on some of them
## OpenCv
Used for image processing
## Pytesseract
Used to read text of image
## gTTS
API of Google translate and TTS
## mms
Really fast libary to grab screenshots
## PIL

## screeninfo
A small cross-platform to grab monitor information so I can guess where to take screenshots
## playsound
A cross-platform way to play the sounds I get from gTTS
