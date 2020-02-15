import requests
from bs4 import BeautifulSoup
import csv
import time



def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    #pages = soup.find('ul', class_ = "pagn").find_all('li', class_ = 'pagn-page', 'a')[-1].get('href=')
    pages = soup.find('ul', class_ = "pagn").find_all('a')[-1].get('href')
    total_pages = pages.split('=')[-1]
    
    return int(total_pages)
def write_csv(data):
    with open('svetofor.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['title'],
                          data['cost'],
                          data['url'],
                          data['link_photo']) )



def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_ = "category-items-outer clearfix list-exp-v3").find_all('article', class_ ="listing-item")
    #ads = soup.find('div', class_ = "category-items-outer clearfix list-exp-v3").find_all('div', class_="listing-item-main")
    #ads = soup.find('div', class_ = "category-items-outer clearfix list-exp-v3").find_all('div', class_ ="mr-3")
    #ads = soup.find('div', class_ = "category-items-outer clearfix list-exp-v3").find_all('div', id_ ="main-listing-block")
    
    
    for ad in ads:
        try:
            title = ad.find('div', class_ = "listing-item-main").find('a').text.strip()
        except:
            title = ""
        try:
            #cost = ad.find('div', class_ = "listing-item-main").find('a').find('p')
            #cost = ad.find('div', class_ = "listing-item-main").find_all('p', class_ = "listing-item-title").text.strip()
            cost = ad.find('div', class_ = "listing-item-main").find('p', class_= "listing-item-title").text.strip()
            #total_cost = cost.split('\xa0')
        except:
            cost = ""
        try:
            url = 'https://lalafo.kg' + ad.find('div', class_ = "listing-item-main").find('a').get('href')
        except:
            url = ""
        try:
            link_photo = ad.find('div', class_ = "listing-item-img-wrap").find('img').get('src')
        except:
            link_photo = ""

        data = {'title': title,
                'cost': cost,
                'url': url,
                'link_photo': link_photo}

        write_csv(data)

def main():
    
    start = time.time()
    url = 'https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnye-telefony/apple-iphone'
    base_url = 'https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnye-telefony/apple-iphone'
    page_part = '?page='
    
    total_pages = get_total_pages(get_html(url))
    
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        # print((url_gen))
        html = get_html(url_gen)
        get_page_data(html)
    finish = time.time()
    result = finish - start
    print("Program run time: " + str(result) + " seconds.")

if __name__ == "__main__":
    main()