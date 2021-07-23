from bs4 import BeautifulSoup
from selenium import webdriver
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
import random
import pickle
# from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
from alegro_user import allegro_email, aleeqro_password

ua = UserAgent()


def parsing_items(driver, urls, vebndor_kode):
    hunter_lst = [vebndor_kode]
    data_result = []
    main_window = driver.current_window_handle
    for item_url in urls:
        time.sleep(random.uniform(5, 20))
        driver.execute_script("window.open();")
        driver.switch_to_window(driver.window_handles[1])
        driver.get(item_url)
        time.sleep(random.uniform(12, 30))
        parametrs = driver.find_elements_by_class_name("_f8818_DQKcc")
        params_list = []
        for param in parametrs:
            params_list.append(param.text.upper().replace(" ", '').strip())
        hunter_set = set(hunter_lst)
        params_set = set(params_list)
        verification = hunter_set.issubset(params_set)
        if verification:
            price = driver.find_element_by_class_name("_9a071_1tOgC").text.split(" ")[0]
            data_result.extend([driver.current_url, price])
            time.sleep(random.uniform(2, 9))
            driver.close()
            driver.switch_to_window(main_window)
            break
        else:
            driver.close()
            driver.switch_to_window(main_window)
    return data_result


def beautiful_finder(driver, vebndor_kode, vendor_title):
    res = []
    articles = driver.find_element_by_class_name("opbox-listing").find_elements_by_tag_name("article")
    for article in articles:
        title = article.text
        for i in article.find_elements_by_tag_name("dd"):
            title += i.text

        text = title.upper().replace(" ", "").strip()
        if vebndor_kode in text and vendor_title in text:
            price = article.find_element_by_class_name("_9c44d_3AMmE").find_element_by_class_name("myre_zn").text.strip(" zł").replace(",", ".")
            item_url = article.find_element_by_class_name("_9c44d_2vTdY").get_attribute("href")
            res.append({"price": float(price),
                        "url": item_url})
    res.sort(key=lambda x: x['price'])
    urls_list = [el["url"] for el in res]

    return urls_list


def allegro(proxy_list, vendor_name, vendor_code):
    pr = random.choice(proxy_list)
    first_part ="https://allegro.pl/listing?string="
    second_part = f"{vendor_code} {vendor_name}".replace(" ", "%20").replace("/", "%2F")
    finder_url = first_part + second_part
    print(finder_url)
    vebndor_kode = vendor_code.strip().replace(" ", "").upper()
    vendor_title = vendor_name.strip().replace(" ", "").upper()

    x = True
    while x:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-javascript")
        # options.add_argument('--no-sandbox')
        options.add_argument('--proxy-server=socks4://' + pr)
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("user-data-dir=//home/stepanenko/.config/google-chrome/Default")
        options.add_argument("dom.webdriver.enabled")

        driver = webdriver.Chrome(
            executable_path="/home/stepanenko/Projects/three_shops/chromedriver", options=options)
        driver.maximize_window()
        try:
            # driver.get(finder_url)
            driver.get('https://proxy6.net/en/myip')
            time.sleep(10)
            # urls = beautiful_finder(driver, vebndor_kode, vendor_title)
            # parsing = parsing_items(driver, urls, vebndor_kode)
        except Exception as ex:
            print(ex)
        else:
            x = False
            # return parsing
        finally:
            driver.close()
            driver.quit()


