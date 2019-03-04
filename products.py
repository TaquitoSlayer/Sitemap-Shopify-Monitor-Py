import requests
import re
import json
import bs4 as bs

r = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}

def generate_sitelist():
    with open('sitelist.txt') as urls:
        sitelist = urls.read().splitlines()
    return sitelist

def List(url, proxy):
    product_urls = []
    sitemap_products = []
    dump = r.get(url, headers = headers, proxies={"http": proxy, "https": proxy})
    soup = bs.BeautifulSoup(dump.text, 'lxml')
    for sitemap in soup.find_all('loc'):
        sitemap_products.append(sitemap.get_text())
    sitemap_products = sitemap_products[0]
    dump_products = r.get(sitemap_products, headers = headers, proxies={"http": proxy, "https": proxy})
    soup = bs.BeautifulSoup(dump_products.text, 'lxml')
    for product in soup.find_all('loc'):
        product_urls.append(product.get_text())
    
    return product_urls


def get_info(url):
    variants = {}
    resp = r.get(url, headers = headers)
    stock = 'N/A'
    image = 'https://i.imgur.com/PheG08Z.jpg'
    title = 'NO NAME FOUND'
    price = 'N/A'
    
    try:
        stock = re.findall(r'''"inventory_quantity":(\d*),''', resp.text)
        stock = stock[0]
    except:
        pass
    try:
        jsonurl = url + '.json'
        resp_json = r.get(jsonurl, headers = headers)
        resp_json = json.loads(resp_json.text)
    except:
        print('ERROR LOADING PRODUCT JSON')
        pass

    try:
        images = resp_json['product']['images']
        images = images[0]
        image = images['src']
    except:
        pass
    try:
        title = resp_json['product']['title']
    except:
        pass
    try:
        prices = resp_json['product']['variants']
        for price in prices:
            price = price['price']
    except Exception as e:
        print(e)
        pass
    try:
        variantz = resp_json['product']['variants']
        if 'kith' in url:
            tags = resp_json['product']['tags']
            tags = re.findall(r'''productsize-(.*)?, productsize-''', tags)
            tags = tags[0].replace('productsize-', '')
            tags = tags.replace('-', '.')
            tags = tags.replace(' ', '')
            tags = tags.split(',')
            for variant in variantz:
                for tag in tags:
                    if tag == variant['title']:
                        vid = variant['id']
                        name = variant['title']
                        variants[vid] = name
                    else:
                        pass
        else:
            for variant in variantz:
                vid = variant['id']
                name = variant['title']
                variants[vid] = name
    except Exception as e:
        print(e)
        variants = {"NO ATC LINK FOUND" : "YOU-PLAYED-YOURSELF"}
    return title, image, stock, price, url, variants