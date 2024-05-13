import multiprocessing
import os
from urllib.parse import urlparse
import requests
from selenium import webdriver
import time
import re
import random
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
import pymysql

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.5162 SLBChan/32'}

option = ChromeOptions()
# option.add_argument('--start-maximized')  # 最大化窗口
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 禁用自动化栏
option.add_experimental_option('useAutomationExtension', False)  # 禁用自动化栏的原理：将window.navigator.webdriver改为undefined。

# 反爬虫特征处理
option.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=option)
conn = pymysql.connect(host='localhost', user='root', database='test_shop', charset='utf8', port=3306)
cur = conn.cursor()

NAME = []
URLS = []
sql1 = 'SELECT name, id FROM article_goods'
cur.execute(sql1)
names_list = cur.fetchall()

# 现在 names_list 是一个元组列表，每个元组包含 name 和 id
# names_list[i][0] 将是第 i 个商品的 name
# names_list[i][1] 将是第 i 个商品的 id

Goods = {
    '手机': ['华为', '苹果', '小米', '三星', '手机'],
    '跑鞋': ['李宁跑鞋', '耐克跑鞋', '安踏跑鞋', '跑鞋'],
    '短袖': ['李宁短袖', '冠军短袖', '耐克短袖', '短袖'],
    '家电': ['格力空调', '美的空调', '美的洗衣机', 'TCL电视', '海尔空调', '奥马冰箱', '家电']
}


def GetDatas(Good, tag):
    driver.get(
        f'https://m.pinduoduo.com/m_goods-list?keyword={Good}')
    print('开始运行')
    time.sleep(2)

    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    print('获取网页数据')
    global NAMES
    # divs = soup.select('.goods-image___vdmkM')[:4]
    # for div in divs:
    #     img_url = div
    #     URLS.append(tag + ': ' + str(img_url))
    #     print(f'Image URL: {img_url}')

    divs = soup.find_all('div', class_='goods-name___23d3H')[:4]
    original_prices = soup.find_all('span', class_='today-price__num___3tnVO')[:4]
    current_prices = soup.find_all('span', class_='today-price__num--group___1l9ll')[:4]
    for div, original_price, current_price in zip(divs, original_prices, current_prices):
        product_desc = div.span.get_text() if div.span else None
        name = tag + ' ' + str(product_desc)
        name = name.replace('/', '_').replace('\\', '_').replace(' ', '_')
        original_price_text = original_price.text
        original_price_clean = original_price_text.replace('￥', '')
        current_price_text = current_price.text
        current_price_clean = current_price_text.replace('￥', '')

        # 使用参数化查询来防止SQL注入
        sql3 = 'INSERT INTO article_goods (name, original_price, current_price) VALUES (%s, %s, %s)'
        values = (name, original_price_clean, current_price_clean)

        try:
            # cur.execute(sql3, values)
            print(f'Inserted: {name}, {original_price_clean}, {current_price_clean}')
        except pymysql.MySQLError as e:
            print(f'Error: {e}')
            print(f'Product Description: {product_desc}')
            print('---')

    conn.commit()


def GetImage(url, name):
    folder = r'E:\python\Django\babala\article\static\images1'
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        safe_file_name = name.replace('/', '_').replace('\\', '_').replace(' ', '_') + ".png"
        file_path = os.path.join(folder, safe_file_name)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f'Image downloaded to {file_path}')
        else:
            print(f'Failed to download image from {url}')
    except Exception as e:
        print(f'An error occurred: {e}')


def GetUrl(names):
    global URLS
    for name, id1 in names:
        try:
            driver.get('https://image.baidu.com/')
            driver.find_element(By.XPATH, '//*[@id="kw"]').send_keys(name)
            driver.find_element(By.XPATH, '//*[@id="homeSearchForm"]/span[2]/input').click()
            time.sleep(1)
            data = driver.page_source
            soup = BeautifulSoup(data, 'lxml')
            div = soup.find('div', class_='imgbox-border')
            img_url = div.img['src']
            GetImage(img_url, str(id1))
            print(img_url)
        except:
            pass



GetUrl(names_list)

driver.quit()
