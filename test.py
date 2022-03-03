import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_rest_data():
    base_url = 'https://burgas.zavedenia.com/restaurant_9'
    flag = True
    num_page = 1
    restaurants = {'restaurants': []}
    while flag:
        response = requests.get(f'{base_url}/{str(num_page)}')
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        all_a_tags = (soup.find_all('a', class_='item-link-desktop ellipsis'))
        next_page = soup.find('div', class_='pagination').find('i', class_='fa fa-chevron-right')
        if next_page.find_parent().has_attr('hidden'):
            flag = False
        num_page += 1
        for a_tag in all_a_tags:
            a_url = a_tag.get('href')
            restaurant_link = f'https://burgas.zavedenia.com{a_url}'
            open_link = urlopen(restaurant_link).read().decode('utf-8')
            html = str(open_link)
            html_soup = BeautifulSoup(html, 'lxml')
            json_f = html_soup.find('script', id='serverApp-state').text
            str_json = json_f.replace('&q;', '"')
            data = json.loads(str_json)
            root = re.search(r'profileKey-\d+', str(data))
            profile_key_root = root.group(0)

            profile_key = data.get(profile_key_root).get('info')
            title = profile_key.get('name')
            image = data.get(profile_key_root).get('pathThumb')
            category = profile_key.get('categories')[0].get('name')
            rating = profile_key.get('stars')
            visits = profile_key.get('visits')
            likes = profile_key.get('ups')
            dislikes = profile_key.get('downs')
            capacity_in = profile_key.get('capacityIn')
            capacity_out = profile_key.get('capacityOut')
            prices = profile_key.get('priceRangeText')
            working_hours = profile_key.get('workingHours')
            phones = profile_key.get('phones')

            description = data.get(profile_key_root).get('info').get('description')
            about = description.get('aboutVenue')
            appropriate_for = description.get('appropriateFor')
            music = description.get('music')
            venue_type = description.get('venueType')
            cuisine = description.get('cuisine')
            facilities = description.get('facilities')
            restaurant = {'title': title, 'image': image, 'category': category, 'rating': rating, 'visits': visits,
                          'likes': likes, 'dislikes': dislikes, 'capacity_in': capacity_in, 'capacity_out': capacity_out,
                          'prices': prices, 'working_hours': working_hours, 'phones': phones, 'about': about,
                          'appropriate_for': appropriate_for, 'music': music, 'venue_type': venue_type, 'cuisine': cuisine,
                          'facilities': facilities}
            restaurants['restaurants'].append(restaurant)

    def write_rest_data():
        with open('answer.json', 'w') as file:
            json.dump(restaurants, file)

    write_rest_data()


get_rest_data()
