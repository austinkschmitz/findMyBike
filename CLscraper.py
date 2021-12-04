# TODO
# Create dependencies


import requests, time, sys, schedule
# https://requests.readthedocs.io/en/master/
from bs4 import BeautifulSoup
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage

# Get list of offers
# https://boise.craigslist.org/search/mca?query=yamaha+raider&purveyor-input=all&search_distance=500&postal=83701
###
# SLC = 'https://saltlakecity.craigslist.org/search/mca?purveyor-input=all&search_distance=1000&max_price=20000'
SLC = 'saltlakecity'
# Boise = 'https://boise.craigslist.org/search/mca?purveyor-input=all&search_distance=500&max_price=20000'
Boise = 'boise'
# Reno = 'https://reno.craigslist.org/search/mca?purveyor-input=all&search_distance=1000&max_price=20000'
Reno = 'reno'
# Portland = 'https://portland.craigslist.org/search/mca?purveyor-input=all&search_distance=1000&max_price=20000'
Portland = 'portland'
# Las_Vegas = 'https://lasvegas.craigslist.org/search/mca?purveyor-input=all&search_distance=1000&max_price=20000'
Las_Vegas = 'lasvegas'

Cities = [SLC, Boise, Reno, Portland, Las_Vegas]
URLS = []
Parts = []
keywords = ['XV1900A', 'raider']

for city in Cities:
    URLS.append(
        'https://' + city + '.craigslist.org/search/mca?purveyor-input=all&search_distance=1000&max_price=20000')
    Parts.append('https://' + city + '.craigslist.org/search/mpa?purveyor-input=all')
    # 'https://boise.craigslist.org/search/mpa?purveyor-input=all'
    # 'https://boise.craigslist.org/search/mpa?query=raider&purveyor-input=all'


def find_bike(url, keyword):
    # URL = 'https://boise.craigslist.org/search/mca?purveyor-input=all&search_distance=500&postal=83701&max_price=20000'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='rows')
    car_elems = results.find_all('li', class_='result-row')
    # Parse each offer tile
    for car_elem in car_elems:
        price_elem = car_elem.find('span', class_='result-price')

        title_elem = car_elem.find('a', class_='result-title hdrlnk')

        # print(title_elem.text.strip())
        # print(price_elem.text.strip())
        # print()
        if title_elem.text.strip().lower().find(keyword) != -1:
            print('FOUND YOU BITCH')
            try:
                url_elem = car_elem.find('a', class_="result-image gallery")['href']
                print(url_elem)
                # Get details of particular offer
                CAR_URL = url_elem
                car_page = requests.get(CAR_URL)
                car_soup = BeautifulSoup(car_page.content, 'html.parser')
                attributes = car_soup.find_all('p', class_='attrgroup')

                # Get attributes
                for attribute in attributes:
                    spans = attribute.find_all('span')
                    for span in spans:
                        text = span.text.strip()
                        print(text)
                        print(text.split(':'))
                        print()
                        # Get offer description
                        posting_body = car_soup.find('section', {"id": "postingbody"})
                        print(posting_body.text)
                        # Open the plain text file whose name is in textfile for reading.
            except:
                url_elem = 'UNABLE TO GET LINK!!!!!!'


def start_job():
    for url in URLS:
        find_bike(url, keywords[0])
        find_bike(url, keywords[1])

    for part in Parts:
        find_bike(part, keywords[0])
        find_bike(part, keywords[1])


def test():
    with open(textfile) as fp:
        # Create a text/plain message
        msg = EmailMessage()
        msg.set_content(fp.read())

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f'The contents of {textfile}'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()


#schedule.every(12).hours.do(start_job())
while True:
#    schedule.run_pending()
    start_job()
    time.sleep(42300)


