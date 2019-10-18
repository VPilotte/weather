import pyttsx3
import feedparser
import signal 
import sys
import html2text
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

	app_running = False
