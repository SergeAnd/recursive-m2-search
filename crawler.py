import requests
from bs4 import BeautifulSoup as BS

base_url = 'https://repo.maven.apache.org'
clean_urls = [base_url + '/maven2/cglib/']

found_root_link = []
found_link = []
rec_found_link = []


def recursive_urls(url, depth):
    if depth == 5:
        rec_found_link.append(url)
    else:
        r = requests.get(url)
        html = BS(r.content, 'html.parser')
        for page_link in html.findAll('a'):
            if (page_link.get('href') != '../') and (page_link.get('href')[-1] == '/'):
                new_link = url + page_link.get('href')
                if (new_link == 'none') or (len(new_link) == 0):
                    rec_found_link.append(url)
                else:
                    rec_found_link.append(new_link)
                    recursive_urls(new_link, depth + 1)


def get_links_from_page(url):
    r = requests.get(url)
    html = BS(r.content, 'html.parser')
    list_links = []
    for page_link in html.findAll('a'):
        if page_link.get('href') != '../':
            if page_link.get('href')[-1] == '/':
                url_added_link = url + page_link.get('href')
                list_links.append(url_added_link)
    for link in list_links:
        found_root_link.append(link)
        if recursive_urls(link,0) != 'none':
            recursive_urls(link, 0)


def recursive_search(urls):
    for url in urls:
        get_links_from_page(url)


recursive_search(clean_urls)

print(rec_found_link)
