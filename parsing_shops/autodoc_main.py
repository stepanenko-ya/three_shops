from selenium import webdriver
import time
from fake_useragent import UserAgent
import random
import csv
import json

ua = UserAgent()


def new_window(iter_items, driver, vendor_name, vendor_kode):
    result = []
    vendor_kode_data = vendor_kode.strip().upper().replace(" ", '')
    trademark = vendor_name.upper().replace(" ", "").strip()
    time.sleep(random.uniform(6, 12))
    main_window = driver.current_window_handle
    for item in iter_items:
        vendor_code = item.find_element_by_class_name("article_number").text.split("Numer artykułu: ")[1].upper().replace(" ", "").strip()
        name_item = item.find_element_by_class_name("name").text.upper().replace(" ", "").strip()
        if trademark in name_item or vendor_kode_data in vendor_code:
            try:
                link = item.find_element_by_class_name("name").find_element_by_tag_name("a").get_attribute("href")
            except:
                pass
            else:
                time.sleep(random.uniform(4, 9))
                driver.execute_script("window.open();")
                driver.switch_to_window(driver.window_handles[1])
                driver.get(link)
                time.sleep(4)
                title = driver.find_element_by_class_name("title").text.strip().upper().replace(" ", '')
                art = driver.find_element_by_class_name("subtitle-art-nummer").text.split("Numer artykułu:")[1].strip().upper().replace(" ", '')
                if vendor_kode_data == art and trademark in title:
                    try:
                        price = driver.find_element_by_class_name('product-new-price').text.split(" ")[0]
                    except:
                        price = "0"
                    result.extend([driver.current_url, price])
                    break
                driver.close()
                driver.switch_to_window(main_window)
    return result


def finder_product(items, driver, vendor_name, vendor_kode):
    if len(items) == 0:
        lst = ["product is out of stock", "0"]
    else:
        iter_items = iter(items)
        data_new_window = new_window(iter_items, driver,  vendor_name, vendor_kode)
        lst = data_new_window
    return lst


def autodoc(proxy_list, vendor_name, vendor_code):
    vendor_kode = vendor_code.replace(" ", "+").upper().strip()
    TM_name = vendor_name.replace(" ", "+").upper().strip()
    finder_url = f"https://www.autodoc.pl/search?keyword={vendor_kode}+{TM_name}"
    print(finder_url)

    x = True
    while x:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument(f"--proxy-server=socks4://{random.choice(proxy_list)}")
        options.add_argument("dom.webdriver.enabled")
        options.add_argument("--enable-javascript")
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("user-data-dir=/home/stepanenko/.config/google-chrome/Default")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(executable_path="/home/stepanenko/Projects/three_shops/chromedriver", options=options)
        try:
            driver.get(finder_url)
            with open("autodoc_cookies.json", 'w') as filehandler:
                json.dump(driver.get_cookies(), filehandler)

            with open("autodoc_cookies.json", 'r') as cookiesfile:
                cookies = json.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
            time.sleep(random.uniform(5, 20))
            items = driver.find_element_by_class_name("js-listing-wrap").find_elements_by_class_name('description')
            product_data = finder_product(items, driver,  vendor_name, vendor_code)
        except Exception as ex:
            print(ex)
        else:
            x = False
            return product_data
        finally:
            driver.close()
            driver.quit()
