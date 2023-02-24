from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
from colors import Colors

URL = 'https://www.amazon.com.br/s'

def validate_url(url_product):
    if 'http' in url_product:
        print(f"\nSearching >> {url_product}...")
        return url_product
    elif len(url_product) < 50:
        print(f"\nSearching >> {url_product}...")
        return url_product
    else:
        print("\nURL or Product invalid.")
        return False

def get_raw_content(target, params):
    with open('https_proxies.txt') as proxy:
        server = proxy.readlines()

    flag = True
    while flag:
        https_proxy = f"https://{server[random.randint(0, len(server) - 1)]}"
        try:
            print("\nProxy Server >> : " + str(https_proxy))
            response = requests.get(target, params=params, proxies={'http': https_proxy}, timeout=10)
            if response.status_code == 200:
                print(f"\n{Colors.GREEN}[OK] Proxy Server{Colors.CYAN}")
                flag = False
                return response.text
            else:
                print(f"\n{Colors.RED}[X] Bad proxy server{Colors.CYAN}")
        except:
            continue

    proxy.close()

def collect_data_url(raw_data):
    print("\nCollecting data...")
    soup = BeautifulSoup(raw_data, 'lxml')

    found_result = soup.find('div', {'class': 'a-section a-spacing-small a-spacing-top-small'})
    print(found_result.text)

    items = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    data = []
    for i in items:
        link = i.find('a', {'class': 'a-link-normal'}, href=True)['href']
        title = i.h2.text

        try:
            rating = i.find('div', {'class': 'a-row a-size-small'}).text.split()[0]
        except AttributeError:
            continue
        
        try:
            price = i.find('span', {'class': 'a-offscreen'}).text
        except AttributeError:
            continue

        data.append({'Index': items.index(i), 'title': title, 'rating': rating, 'price': price, 'link': link})

    return data

def save_file(data):
    df = pd.DataFrame(data=data)
    df.to_csv('data_url.csv')

def main():
    PRODUCT = str(input("Type the name of the product: "))
    PAYLOAD = {f'k': {PRODUCT.lower()}}
    raw_data = get_raw_content(URL, PAYLOAD)
    data = collect_data_url(raw_data)
    save_file(data)

if __name__ == '__main__':
    main()