from bs4 import BeautifulSoup
import requests
import json

# Script to scrap apartment data and pass it onto the database.

class Apartment(object):
    name = ""
    number = ""
    building = ""
    status = ""
    price = ""
    bedrooms = ""
    floor = ""
    area = 0

def scrape_data():

    def get_clean_tag_value(tag,attribute):
        tag_data = tag.find(class_=attribute)
        dirty_value = list(tag_data.children)[0]
        value = dirty_value.replace("\n", "")
        return value

    def price_to_int(string):
        print('Price received: ', string)
        if string == '–':
            return 0
        else:
            newstring = string.replace('£','').replace(',','')
            return newstring

    def area_to_float(string):
        return string[:-2]

    urls = [
        'https://anthology.london/developments/deptford-foundry/homes?price=000000-975000&area_units=sqm&order=price_desc',
        'https://anthology.london/developments/deptford-foundry/homes/p2?price=000000-975000&amp;area_units=sqm&amp;order=price_desc',
        'https://anthology.london/developments/deptford-foundry/homes/p3?price=000000-975000&amp;area_units=sqm&amp;order=price_desc',
        'https://anthology.london/developments/deptford-foundry/homes/p4?price=000000-975000&amp;area_units=sqm&amp;order=price_desc',
        'https://anthology.london/developments/deptford-foundry/homes/p5?price=000000-975000&amp;area_units=sqm&amp;order=price_desc',
        'https://anthology.london/developments/deptford-foundry/homes/p6?price=000000-975000&amp;area_units=sqm&amp;order=price_desc',
        'https://anthology.london/developments/deptford-foundry/homes/p7?price=000000-975000&amp;area_units=sqm&amp;order=price_desc',
        'https://anthology.london/developments/deptford-foundry/homes/p8?price=000000-975000&amp;area_units=sqm&amp;order=price_desc'
        ]

    scrapped_apartments = []

    for url in urls:
        print("Accesssing: ", url)
        session = requests.Session()
        request = session.get(url)
        web_html = request.text

        soup = BeautifulSoup(web_html, 'html.parser')

        available_tags = soup.find_all("div", class_="unit deptford-foundry available")
        reserved_tags = soup.find_all("div", class_="unit deptford-foundry reserved")
        # sold_tags = soup.find_all("div", class_="unit deptford-foundry sold")
        apartments_tags = available_tags + reserved_tags

        # Kiekvienam butui sukuriamas objectas ir jam priskiriama data
        for tag_data in apartments_tags:
            apartment = Apartment()

            apartment.number = get_clean_tag_value(tag_data, "unit-home")
            apartment.building = get_clean_tag_value(tag_data, "unit-building")
            apartment.price = price_to_int(get_clean_tag_value(tag_data, "unit-content unit-price"))
            print('Price returned: ', apartment.price)
            apartment.bedrooms = get_clean_tag_value(tag_data, "unit-rooms")
            apartment.floor = get_clean_tag_value(tag_data, "unit-floor")
            apartment.area = get_clean_tag_value(tag_data, "unit-measurement")[:-2]
            apartment.name = apartment.building + ' ' + apartment.number

            tag_status = tag_data.find("div", class_="unit-content unit-availability")
            dirty_status = str(list(tag_status.children)[1]).split("</div>")[1]
            apartment.status = dirty_status.translate({ord(c):None for c in ' \n\t\r'})

            # print("Adding apartment: ", apartment.name)
            scrapped_apartments.append(apartment)

    json_obj = json.dumps([apt.__dict__ for apt in scrapped_apartments], ensure_ascii=True)
    print("JSON encoded: ", json_obj)
    return json_obj
