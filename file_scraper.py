from bs4 import BeautifulSoup
import pandas as pd
import os

URL = 'https://www.amazon.com.br/s'

def collect_data_file(file_path):
    with open(f'{file_path}', 'r') as html:
        soup = BeautifulSoup(html, 'lxml')

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

    html.close()
    return data

def save_file(data):
    df = pd.DataFrame(data=data)
    df.to_csv('data_file.csv')

def validate_path(file_path):
    if os.path.isfile(file_path):
        return True
    return False

def main():
    data = collect_data_file()
    save_file(data)

if __name__ == '__main__':
    main()
