import pandas as pd
from file_scraper import collect_data_file, validate_path
from url_scraper import get_raw_content, collect_data_url, validate_url
from colors import Colors


def line_separator():
    print("\n---------------------------------")

while True:
    line_separator()
    print(
    f""" 
        {Colors.CYAN}\n(1) SCRAPE FROM FILE
        \n(2) SCRAPE FROM URL or By Product Name
        \n{Colors.RED}(3) Exit{Colors.YELLOW}
    """)
    try:
        
        answer = int(input())
    except ValueError:
        continue

    if answer == 1:
        print(f"{Colors.CYAN}\nPaste the file location: ")
        file_path = str(input())
        if validate_path(file_path) == False:
            print("\nFile not found!")
            continue

        data_file= collect_data_file(file_path)
        print(f"\n{Colors.ITALIC}Saving CSV file...")
        df = pd.DataFrame(data=data_file)
        df.to_csv('data_file.csv')
        print(f"\n{Colors.GREEN}Done!")
    elif answer == 2:
        print(f"\n{Colors.CYAN}Paste the URL or the Product name: ")
        target = str(input())
        url_product = validate_url(target) 
        if url_product == False:
            continue

        if 'http' in url_product:
            content = get_raw_content(target, None)
            data_url = collect_data_url(content)
        else:
            PAYLOAD = {f'k': {url_product.lower()}}
            URL = 'https://www.amazon.com.br/s'
            content = get_raw_content(URL, PAYLOAD)
            data_url = collect_data_url(content)

        print("\nSaving CSV file...")
        df = pd.DataFrame(data=data_url)
        df.to_csv('data_url.csv')
        print(f"\n{Colors.GREEN}Done!")
    elif answer == 3:
        break
    else:
        print("Invalid option!")





