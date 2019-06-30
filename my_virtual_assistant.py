import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import requests
from pprint import pprint
import smtplib
import speech
from bs4 import BeautifulSoup
from lib.google_search_results import GoogleSearchResults
import json
import itertools
import logging
import uuid
from urllib.request import urlopen, Request
from urllib.error import URLError
from bs4 import NavigableString
from random import randint
import sys
from playsound import playsound

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# this is the language code in which jarvis speaks i.e hi = hindi , eng-in = english(india)


lang1 = 'en-IN'
lang2 = 'hi'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    

    if hour >= 0 and hour < 12:

        speak("Good Morning ")
        #speech.ttspeech("शुभ प्रभात", lang2)

    elif hour >= 12 and hour <= 18:

        speak(" Good Afternoon ")
        #speech.ttspeech("शुभ दिन", lang2)

    else:

        speak("Good Evening ")
        #speech.ttspeech("शुभ रात्रि", lang2)

    #speech.ttspeech("नमस्ते मैं इको  हूँ मैं आपकी मदद कैसे कर सकती हूँ ", lang2)
    # speech.ttspeech("hi i am jarvis your virtual assistant..HOW MAY i HELP YOU sir", lang1)
    speak("HI I AM echo your voice assistant..HOW MAY I HELP YOU ")


def takecommand():
    """ this is a function of converting speech to text in english language using google voice  """

    r = sr.Recognizer()
    with sr.Microphone() as source:

        print(" LISTENING.....")
        speak("listening you..")
        r.energy_threshold = 300
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:

        print(" Recognizing....")
        speak('recognizing you..please wait for a moment')
        query = r.recognize_google(audio, language='en-IN')
        print(f"user said: {query} \n")

    except Exception as e:

        print(" say that again please ")
        speak('say that again please ')
        # speech.ttspeech("कृपया फिर से कहें ",lang2)
        return 'None'

    return query


def command_hindi():
    
    """ this is a function of converting speech text into हिंदी भाषा """

    r = sr.Recognizer()
    with sr.Microphone() as source:

        #print(" सुन रही हूँ  ")
        #speak("listening you..")
        speech.ttspeech(" सुन रही हूँ ", lang2)
        print(" सुन रही हूँ  ")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:

        #print(" समज रही हूँ ...")
        #speak('recognizing you..please wait for a moment')
        speech.ttspeech(" समज रही हूँ ...", lang2)
        print(" समज रही हूँ ...")
        query = r.recognize_google(audio, language='HI')
        print(f"आपने कहा : {query} \n")

    except Exception as e:

        #print(" कृपया फिर से कहें  ")
        #speak('say that again please ')
        speech.ttspeech("कृपया फिर से कहें ", lang2)
        print(" कृपया फिर से कहें  ")
        return 'None'

    return query


def takecommand1():
    r = sr.Recognizer()
    with sr.Microphone() as source:

        print(" LISTENING.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:

        print(" Recognizing....")
        speak('recognizing you..please wait for a moment')
        query1 = r.recognize_google(audio, language='en-IN')

        # print( f"user said: {query1} \n")

    except Exception as e:

        print(" say that again please ...")
        speak('say that again please ')
        return 'None'

    return query1


def takecommand2():
    r = sr.Recognizer()
    with sr.Microphone() as source:

        print(" LISTENING.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:

        print(" Recognizing....")
        speak('recognizing you..please wait for a moment')
        query2 = r.recognize_google(audio, language='en-IN')
        # print( f"user said: {query1} \n")

    except Exception as e:

        print(" say that again please ...")
        speak('say that again please ')
        return 'None'

    return query2


# image download from google functions starts from heare

def configure_logging():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()

    handler.setFormatter(

        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))

    logger.addHandler(handler)

    # Path to your LOG FILE.

    Filehandler = logging.FileHandler(
        "F:\\voice assistant\\log.txt")  # path of your log file

    Filehandler.setFormatter(

        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))

    logger.addHandler(Filehandler)

    return logger


logger = configure_logging()

REQUEST_HEADER = {

    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


def get_soup(url, header):
    response = urlopen(Request(url, headers=header))

    return BeautifulSoup(response, 'html.parser')


def get_query_url(query):
    return "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query


def extract_images_from_soup(soup):
    image_elements = soup.find_all("div", {"class": "rg_meta"})

    metadata_dicts = (json.loads(e.text) for e in image_elements)

    link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)

    return link_type_records


def extract_images(query, num_images):
    url = get_query_url(query)

    logger.info("Souping")

    soup = get_soup(url, REQUEST_HEADER)

    logger.info("Extracting image urls")

    link_type_records = extract_images_from_soup(soup)

    return itertools.islice(link_type_records, num_images)


def get_raw_image(url):
    req = Request(url, headers=REQUEST_HEADER)

    resp = urlopen(req)

    return resp.read()


def save_image(raw_image, image_type, save_directory):
    extension = image_type if image_type else 'jpg'

    file_name = uuid.uuid4().hex + "." + extension

    save_path = os.path.join(save_directory, file_name)

    with open(save_path, 'wb') as image_file:
        image_file.write(raw_image)


def download_images_to_dir(images, save_directory, num_images):
    for i, (url, image_type) in enumerate(images):

        try:

            logger.info("Making request (%d/%d): %s", i, num_images, url)

            raw_image = get_raw_image(url)

            save_image(raw_image, image_type, save_directory)

        except Exception as e:

            logger.exception(e)


def run(query, save_directory, num_images):
    query = '+'.join(query.split())

    logger.info("Extracting image links")

    images = extract_images(query, num_images)

    logger.info("Downloading images")

    download_images_to_dir(images, save_directory, num_images)

    logger.info("Finished")


def main1(q, num):
    q = q
    num = num
    loc = 'F:\\voice assistant\\images'

    run(q, loc, num)


# end of image download functions


if __name__ == '__main__':

    wishme()

    while (1):

        speak('choose your language english or hindi for giving command..')
        lanquery = takecommand().lower()
        print(lanquery)

        if lanquery == 'hindi':

            while (1):

                hindiquery = command_hindi()

                if "यूट्यूब" in hindiquery:

                    wb.get(chrome_path).open('www.youtube.com')

                elif 'कृपया भाषा बदलें' in hindiquery:

                    break

                elif "फेसबुक" in hindiquery:

                    wb.get(chrome_path).open('www.facebook.com')

                elif "गूगल" in hindiquery:

                    wb.get(chrome_path).open('www.google.com')

                elif "गाना सुनाओ" in hindiquery:

                    latest = 'F:\\music\\latest'
                    songs = os.listdir(latest)
                    myno = random.choice(range(0, len(songs)))
                    os.startfile(os.path.join(latest, songs[myno]))

                elif "गाना बंद" in hindiquery:

                    os.system('TASKKILL /F /IM wmplayer.exe')

                elif "टि्वटर" in hindiquery:

                    wb.get(chrome_path).open('www.twitter.com')

                elif "ट्विटर" in hindiquery:

                    wb.get(chrome_path).open('www.twitter.com')

                elif "समय" in hindiquery:

                    mytime = datetime.datetime.now().strftime("%I:%M:%S %p")
                    mydate = datetime.datetime.now().strftime("%a, %b, %d, %Y")
                    speech.ttspeech("समय है", lang2)
                    speak(mytime)
                    speech.ttspeech("दिनांक है", lang2)
                    speak(mydate)

        elif lanquery == 'english':

            while (1):

                query = takecommand().lower()

                # logics for executing tasks as per query

                if 'wikipedia' in query:

                    speak('Searching Wikipedia...')
                    query = query.replace("Wikipedia", " ")
                    result = wikipedia.summary(query, sentences=2)
                    speak("according to wikipedia ...")
                    print(result)
                    # speak(result)
                    speech.ttspeech(result, lang='en-in')

                elif 'open youtube' in query:

                    wb.get(chrome_path).open("www.youtube.com")

                elif 'change language' in query:

                    break

                elif "quit" in query:

                    sys.exit()

                elif 'open facebook' in query:

                    wb.get(chrome_path).open("www.facebook.com")

                elif 'open stackoverflow' in query:

                    wb.get(chrome_path).open('www.stackoverflow.com')

                elif 'open geek for geeks' in query:

                    wb.get(chrome_path).open('www.geeksforgeeks.org')

                elif 'open google' in query:

                    wb.get(chrome_path).open('www.google.com')

                elif 'open instagram' in query:

                    wb.get(chrome_path).open('www.instagram.com')

                elif 'open twitter' in query:

                    wb.get(chrome_path).open('www.twitter.com')

                elif "open linkedin" in query:

                    wb.get(chrome_path).open('https://in.linkedin.com/')

                elif 'play music' in query:

                    latest = 'F:\\music\\latest'
                    songs = os.listdir(latest)
                    myno = random.choice(range(0, len(songs)))
                    os.startfile(os.path.join(latest, songs[myno]))

                elif 'open music' in query:

                    latest = 'F:\\music\\latest'
                    songs = os.listdir(latest)
                    myno = random.choice(range(0, len(songs)))
                    os.startfile(os.path.join(latest, songs[myno]))

                elif 'time' in query:

                    mytime = datetime.datetime.now().strftime("%I:%M:%S %p")
                    mydate = datetime.datetime.now().strftime("%a, %b, %d, %Y")
                    speak(f"sir , the time is {mytime}")
                    speak(f"sir , the date is {mydate}")

                elif 'open pycharm' in query:

                    pypath = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2019.1.2\\bin\\pycharm64.exe"
                    os.startfile(pypath)

                elif 'close pycharm' in query:

                    speak('closing pycharm')
                    os.system('taskkill /f /im pycharm.exe')

                elif 'close chrome' in query:

                    speak('closing google chrome')
                    os.system('taskkill /f /im chrome.exe')

                elif 'stop music' in query:

                    speak('closing music')
                    os.system('TASKKILL /F /IM wmplayer.exe')

                elif 'close music' in query:

                    speak('closing music')
                    os.system('TASKKILL /F /IM wmplayer.exe')

                elif 'open pubg' in query:

                    speak('opening pubge')
                    pubgpath = "G:\\Program Files\\TxGameAssistant\\AppMarket\\AppMarket.exe"
                    os.startfile(pubgpath)

                elif 'close pubg' in query:

                    speak('closing pubge')
                    os.system('TASKKILL /F /IM AppMarket.exe')

                elif 'shutdown' in query:

                    # this will shutdown the system in 5 seconds

                    speak('your system will shutdown in 5 seconds')
                    os.system('shutdown /s /t 5')

                elif 'weather' in query:

                    speak('which city weather you want to know')

                    query1 = takecommand1().lower()

                    city = query1
                    print(city)

                    if city == 'pauri garhwal':
                        url = "http://api.openweathermap.org/data/2.5/weather?appid=72e0ab27553c1e0279c6e68ee4d226a7&q=pauri&units=metric"
                        res = requests.get(url)
                        data = res.json()
                        pprint(data)

                        temp = data['main']['temp']
                        windspeed = data['wind']['speed']
                        weather = data['weather'][0]['description']
                        pressure = data['main']['pressure']
                        humidity = data['main']['humidity']
                        latitude = data['coord']['lat']
                        longitude = data['coord']['lon']

                        speak(f'{city} city all weather details are ')
                        speak(f'temperature is {temp} degree celcius ')
                        speak(f"windspeed is {windspeed} kilometer per hour ")
                        speak(f"weather condition is {weather}")
                        speak(f"pressure is {pressure} pascal ")
                        speak(f"humidity is {humidity} grams per cubic meter ")
                        speak(
                            f'position on google map is..latitude value is {latitude} and longitude value is {longitude}')
                        continue

                    url = "http://api.openweathermap.org/data/2.5/weather?appid=72e0ab27553c1e0279c6e68ee4d226a7&q={}&units=metric".format(
                        city)
                    res = requests.get(url)
                    data = res.json()
                    pprint(data)

                    temp = data['main']['temp']
                    windspeed = data['wind']['speed']
                    weather = data['weather'][0]['description']
                    pressure = data['main']['pressure']
                    humidity = data['main']['humidity']
                    latitude = data['coord']['lat']
                    longitude = data['coord']['lon']

                    speak(f'{city} city all weather details are ')
                    speak(f'temperature is {temp} degree celcius ')
                    speak(f"windspeed is {windspeed} kilometer per hour ")
                    speak(f"weather condition is {weather}")
                    speak(f"pressure is {pressure} pascal ")
                    speak(f"humidity is {humidity} grams per cubic meter ")
                    speak(
                        f'position on google map is..latitude value is {latitude} and longitude value is {longitude}')

                elif 'email' in query:

                    speak('email is ready to sent please tell recipient address')
                    email = 'naveenrawat808@gmail.com'
                    password = os.environ.get('password')
                    query2 = takecommand2().lower()
                    recevier_address = query2.replace(" ", "")
                    print(recevier_address)

                    try:

                        with smtplib.SMTP('smtp.gmail.com', 25) as smtp:

                            smtp.ehlo()
                            smtp.starttls()
                            smtp.login(email, password)

                            speak('whats the subject')
                            query3 = takecommand2().lower()
                            subject = query3
                            speak(
                                'now tell me the content of email you want to send')
                            query4 = takecommand2().lower()
                            body = query4

                            msg = f"subject : {subject}\n\n{body}"

                            smtp.sendmail(email, recevier_address, msg)
                            smtp.close()
                            print('email sent successfully')
                            speak('email sent successfully')

                    except Exception as e:

                        print("message is not sent plese try again")
                        speak('message is not sent please try again')

                elif 'website' in query:

                    speak('give your website name')

                    query5 = takecommand2().lower()
                    wb.get(chrome_path).open(f'www.{query5}.com')

                elif "search youtube" in query:

                    speak('tell me what you want to search in youtube')
                    query6 = takecommand2().lower()
                    wb.get(chrome_path).open(
                        'https://www.youtube.com/results?search_query={}'.format(query6))

                elif 'download' in query:

                    speak(' what type of images you want to download from google..')

                    query7 = takecommand2().lower()
                    print(query7)

                    speak("please tell number of images you want to download ")

                    query8 = takecommand2()
                    query9 = int(float(query8))

                    print(query9)

                    speak("image downloading in progress plese wait for a moment...")

                    main1(query7, query9)

                    speak('all images downloaded successfully...')

                elif "joke" in query:

                    url = "http://www.goodbadjokes.com"

                    try:
                        with urlopen(url) as request:

                            data = request.read()

                    except URLError:

                        print("their is an error opening this url{}".format(url))
                        exit(1)

                    soup = BeautifulSoup(data, 'html.parser')

                    joke_containers = soup.findAll(
                        'div', {"class": "joke-body-wrap"})

                    jokes = []

                    for joke_container in joke_containers:

                        joke = []

                        for line in joke_container.findChildren('a', {"class": "permalink"})[0].contents:

                            if type(line) == NavigableString:

                                clean_lines = (str(line),)

                            else:

                                clean_lines = line.stripped_strings

                            for clean_line in clean_lines:

                                if clean_line:
                                    joke.append(clean_line.strip("\n\r"))

                    if joke:
                        jokes.append(joke)

                    myjoke = "\n\t> ".join(jokes[randint(0, len(jokes) - 1)])
                    print(myjoke)
                    speak(myjoke)
                    playsound('Crowd-laughing.mp3')

                elif "news" in query:

                    url = "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=339e2f8db25644938177faafa696856b"

                    res = requests.get(url)

                    data = res.json()

                    news_title1 = data['articles'][1]['title']
                    news_content1 = data["articles"][1]['description']

                    news_title2 = data["articles"][2]['title']
                    news_content2 = data["articles"][2]["description"]

                    print(f"Title is :{news_title1}\n")
                    speak(news_title1)
                    print(f"Content of news is :{news_content1}\n")
                    speak(news_content1)

                    print(f"Title is : {news_title2}\n")
                    speak(news_title2)
                    print(f"Content of news is :{news_content2}")
                    speak(news_content2)
