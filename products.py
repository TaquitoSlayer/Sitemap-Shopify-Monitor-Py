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
    if 'kith' in url:
        sitemap_productz = sitemap_products[1]
        dump_products = r.get(sitemap_productz, headers = headers, proxies={"http": proxy, "https": proxy})
        soup = bs.BeautifulSoup(dump_products.text, 'lxml')
        for product in soup.find_all('loc'):
            product_urls.append(product.get_text())
        sitemap_productz = sitemap_products[0]
        dump_products = r.get(sitemap_productz, headers = headers, proxies={"http": proxy, "https": proxy})
        soup = bs.BeautifulSoup(dump_products.text, 'lxml')
        for product in soup.find_all('loc'):
            product_urls.append(product.get_text())  
    else:
        sitemap_products = sitemap_products[0]
        dump_products = r.get(sitemap_products, headers = headers, proxies={"http": proxy, "https": proxy})
        soup = bs.BeautifulSoup(dump_products.text, 'lxml')
        for product in soup.find_all('loc'):
            product_urls.append(product.get_text())
    product_urls = list(set(product_urls))
    return product_urls

def List2():
    product_urls = []
    # sitemap_products = []
    # dump = r.get(url, headers = headers, proxies={"http": proxy, "https": proxy})
    with open('sitemap2.xml') as sitemap:
        soup = bs.BeautifulSoup(sitemap, 'lxml')
        for product in soup.find_all('loc'):
            product_urls.append(product.get_text())
    
    return product_urls

def List3():
    product_urls = []
    # sitemap_products = []
    # dump = r.get(url, headers = headers, proxies={"http": proxy, "https": proxy})
    with open('sitemap.xml') as sitemap:
        soup = bs.BeautifulSoup(sitemap, 'lxml')
        for product in soup.find_all('loc'):
            product_urls.append(product.get_text())
    
    return product_urls


def get_info(url, proxy):
    variants = {}
    resp = r.get(url, headers = headers, proxies={"http": proxy, "https": proxy})
    # resp = r.get(url, headers = headers)
    try:
        stock = re.findall(r'''"inventory_quantity":(\d*),''', resp.text)
        stock = stock[0]
    except:
        stock = 'N/A'
        pass
    try:
        jsonurl = url + '.js'
        resp_json = r.get(jsonurl, headers = headers, proxies={"http": proxy, "https": proxy})
        resp_json = json.loads(resp_json.text)
    except:
        print('ERROR LOADING PRODUCT JSON')
        pass

    try:
        image = resp_json['images'][0]
        image = f'https:{image}'
    except:
        image = 'https://i.imgur.com/PheG08Z.jpg'
        pass
    
    try:
        title = resp_json['title']
    except:
        title = 'NO NAME FOUND'
        pass
    try:
        prices = resp_json['variants']
        for price in prices:
            price = price['price']
    except Exception as e:
        print(e)
        price = 'N/A'
        pass
    try:
        variantz = resp_json['variants']             
        for variant in variantz:
            if variant['available'] == True:
                vid = variant['id']
                name = variant['title']
                variants[vid] = name
            else:
                pass
    except Exception as e:
        print(f'ERROR: {e}')
    return title, image, stock, price, url, variants