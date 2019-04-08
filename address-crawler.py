import re
import requests
import configparser
from lxml import etree

configuration = configparser.ConfigParser()
configuration.read("app.conf")
config = configuration['address-crawler']

page_start = int(config['page_start']) - 1
page_count = int(config['page_count'])
page_size = 25
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
headers = {"User-Agent": user_agent}
url_format = "https://memo.sv/profiles/most-actions?&offset={}"

addresses = []
for i in range(0, page_count):
    url = url_format.format(page_size * (i + page_start))
    print(url)
    html = etree.HTML(requests.get(url, headers=headers).text)
    profile_list = html.xpath('//div[@class="narrow-content"]//a[@class="profile profile-link"]')
    for profile in profile_list:
        match = re.match(r'profile/(.+)', profile.attrib['href'])
        if len(match.groups()) == 1:
            addresses.append(match.group(1))

with open('send.address', 'w', encoding='utf-8') as file:
    for address in addresses:
        file.writelines(address + '\n')
