import pyttsx3
import feedparser
import signal 
import sys
import html2text
import speech_recognition as sr
from threading import Thread

app_running = True

engine = pyttsx3.init()

url = "https://weather.gc.ca/rss/city/qc-147_f.xml"

# Handles Ctrl + Z
def handler(signum, frame):
	engine.stop()
	sys.exit()

def read(text):
	engine.say(text)
	engine.runAndWait()


while app_running:

	signal.signal(signal.SIGTSTP, handler)

	feed = feedparser.parse(url)

	for x in range(0, len(feed.entries)):
		engine.setProperty('voice', 'com.apple.speech.synthesis.voice.amelie')
		engine.setProperty('rate', engine.getProperty('rate') - 30)

		t = Thread(target=read(feed.entries[x].summary))
		t.start()

		#engine.say(feed.entries[x].title)
		#engine.say(html2text.html2text(feed.entries[x].summary))
		#engine.run()

	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
		try:
			print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language='fr-CA'))
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

	app_running = False
