import requests
from bs4 import BeautifulSoup
import csv

url = 'http://www.hclib.org/about/locations'
output = 'hclib-locations.csv'

response = requests.get(url)
html = response.text
page = BeautifulSoup(html)

header = ('location', 'location_url', 'phone', 'street', 
          'city', 'zipcode', 'address_url',
          'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
          
with open(output, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for item in page.find_all('div', class_='locations-list__item'):
        title_elt = item.find('div', class_='locations-list__title')
        a1, a2 = title_elt.find_all('a')
        location = a1.text
        location_url = a1.get('href')
        phone = a2.text
        # print (location, location_url, phone)
   
        elt = item.find('div', class_='locations-list__address')
        elt = elt.find('a')
        address_url = elt.get('href')
        contents = elt.contents
        street = contents[0]
        city = contents[2].split(',', 1)[0]
        zipcode = contents[2][-5:]
   
        times = item.find('table', 'locations-list__times')
        hours = [day.text.encode('utf-8') for day in times.find_all('td')][:7]
   
        row = [location, location_url, phone, street, 
               city, zipcode, address_url] + hours
        print row
        writer.writerow(row)
   
          
   
