import sys
import re
import argparse
import requests
from bs4 import BeautifulSoup

author = "__Bryan__"


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', help='url for input. NEEDS TO BE HTTP://YOUR_URL')

    return parser


def main():

    parser = create_parser()
    args = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(1)

    if not args.text.startswith('http'):
        print("Url not correct format\nhttp://{}.com\n".format(args.text))
        sys.exit(1)

    response = requests.get(args.text).text

    soup = BeautifulSoup(response, 'lxml')

    img_list = soup.findAll('img')  # All <img> tags
    anchor_list = soup.findAll('a')  # All <a> tags
    url_list = []

    for img in img_list:
        try:
            url_list.append(img['src'])

        except Exception as e:
            url_list.append('none')

    for anchor in anchor_list:
        try:
            url_list.append(anchor['src'])
        except Exception as e:
            url_list.append('none')

    poo = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response)
    for each in poo:
        url_list.append(each)

    print(set(url_list))

    email_list = re.findall(r'info@[a-zA-Z0-9.]+', response)
    print(set(email_list))

    phone_list = re.findall(r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?', response)
    print(set(phone_list))


if __name__ == '__main__':
    print("\n")
    main()
    print("\n")
