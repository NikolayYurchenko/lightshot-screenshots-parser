# libraries modules
from time import sleep
from urllib3.exceptions import HTTPError
from bs4 import BeautifulSoup
import requests
import random

# config file
import config


def do_requests_by_range():
    for item in range(config.requests_range):
        try:
            # Generate random id and request to get html
            proxy = {'http': random.choice(config.proxies)}
            image_id = generate_image_id()
            link = 'https://prnt.sc/' + image_id
            print ("Request to  " + link)
            response = requests.get(link, headers={'User-Agent': config.user_agent}, proxies=proxy)

            # Parse response html and find image
            soap = BeautifulSoup(response.text, 'html.parser')
            first_img_url = soap.find_all('img')[0].get('src')

            # Get image bytes by source
            image = {}
            try:
                image = requests.get(first_img_url)
                print("Success find image by source - " + first_img_url)
            except:

                print ("Failed request to get image by url - " + first_img_url)
                sleep(random.randint(5, 9))
                do_requests_by_range()

            # Write file and save
            out = open(config.store_path + "/{in_img}.png".format(in_img=image_id), "wb")
            out.write(image.content)
            out.close()
            print ("Success write image as file, image - " + first_img_url)
            sleep(random.randint(5, 9))

        except HTTPError as httpError:
            print("request failed, cause = " + str(httpError))


def generate_image_id():
    image_id = ''
    for item in range(config.id_length):
        image_id += random.choice(config.symbols)

    return image_id


def main():
    do_requests_by_range()


if __name__ == main():
    main()
