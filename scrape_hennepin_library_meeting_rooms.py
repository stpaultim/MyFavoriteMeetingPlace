import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = 'http://www.hclib.org'
OUTPUT_FILE = 'hennepin-library-rooms.csv'

def get_page(url):
    r = requests.get(url)
    html = r.text
    page = BeautifulSoup(html)
    return page

def get_room_list():
    url = BASE_URL + '/about/meeting-rooms'
    page = get_page(url)
    rooms = page.find_all('div', class_='meeting-room-listing')
    return rooms

def parse_room(room):
    image_div = room.find('div', class_='listing__img')
    image_tag = image_div.find('img')
    image_url = BASE_URL + image_tag.get('src')
    
    content = room.find('div', class_='listing__content')
    location = content.find('h3').text
    
    list_items = content.find_all('li')
    room_name = list_items[0].text
    group_size = list_items[2].text
    anchor = content.find_all('a')[1]
    detail_url = BASE_URL + anchor.get('href')
    
    page = get_page(detail_url)
    content = page.find('div', class_='main-content')
    description = content.find_all('p')[1].text.encode('utf-8')
    
    return (location, room_name, group_size, description, 
            image_url, detail_url)

if __name__ == '__main__':
    header_row = ['location', 'room_name', 'group_size', 'description',
                  'image_url', 'detail_url']
    with open(OUTPUT_FILE, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header_row)
        for room in get_room_list():
            row = parse_room(room)
            print (row)
            writer.writerow(row)
    
    
    
    