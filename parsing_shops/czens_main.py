from selenium import webdriver
import time
from fake_useragent import UserAgent
import random
import json
from selenium.webdriver.common.keys import Keys
import pickle


ua = UserAgent()


def new_window(iter_items, driver, vendor, vendor_kode):
    result = []
    for item in iter_items:
        main_window = driver.current_window_handle
        time.sleep(3)
        name = item.find_element_by_class_name(
            "description").find_element_by_class_name("ga-click").text.upper().strip().replace(" ", '')
        vendor_code = item.find_element_by_class_name(
            "description").find_element_by_class_name("nr").text.upper().strip().replace(" ", '').split(":")[1]
        if vendor.replace(" ", '').upper().strip() in name or vendor_kode.replace(" ", '').upper().strip() in vendor_code:
            try:
                url = item.find_element_by_class_name("description").find_element_by_class_name("ga-click").get_attribute(
                "href")
            except:
                pass
            else:
                time.sleep(4)
                driver.execute_script("window.open();")
                driver.switch_to_window(driver.window_handles[1])
                driver.get(url)
                time.sleep(4)
                acticle = driver.find_element_by_class_name(
                    "pkw-product__artikel").text.split("Artykuł №: ")[1].upper().replace(" ", '').strip()
                title = driver.find_element_by_class_name(
                    "pkw-product__name").find_element_by_tag_name("h2").text.replace(" ", "").upper().strip()
                if vendor_kode.replace(" ", '').upper().strip() == acticle and vendor.replace(" ", '').upper().strip() in title:
                    try:
                        price = driver.find_element_by_class_name('pkw-product__price').text.split(" ")[0]
                        print(price)
                    except:
                        price = "0"
                    result.extend([driver.current_url, price])
                    break
                driver.close()
                driver.switch_to_window(main_window)
    return result


def finder_product(items, driver, vendor, vendor_kode):
    if len(items) == 0:
        lst = ["product is out of stock", "0"]
    else:
        iter_items = iter(items)
        funk_result_new_window = new_window(iter_items, driver, vendor, vendor_kode)
        lst = funk_result_new_window
    return lst


def czesciauto(vendor_name, vendor_code):
    result = None
    vendor_title = vendor_name.upper().strip().title().replace(" ", "+")
    venor_kod = vendor_code.replace(" ", "+")

    url = f"https://www.czesciauto24.pl/search?keyword={venor_kod}+{vendor_title}"
    print(url)
    proxy_list = open("prox_adress").read().split("\n")

    x = True
    while x:
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--proxy-server=socks4://' + random.choice(proxy_list))
        options.add_argument("--enable-javascript")
        options.add_argument('--no-sandbox')
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("user-data-dir=/home/stepanenko/.config/google-chrome/Default")
        options.add_argument("dom.webdriver.enabled")

        driver = webdriver.Chrome(executable_path="/home/stepanenko/Projects/three_shops/chromedriver",
                                  options=options)

        try:
            driver.get(url)
            with open("czesc_cookies", 'w') as filehandler:
                json.dump(driver.get_cookies(), filehandler)

            with open("czesc_cookies", 'r') as cookiesfile:
                cookies = json.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
            time.sleep(random.uniform(9, 30))
            items = driver.find_element_by_class_name("listing_items").find_elements_by_class_name('brand-products')
            product_data = finder_product(items, driver, vendor_name, vendor_code)

        except Exception as ex:
            print(ex)
        else:
            x = False
            return product_data
        finally:
            driver.close()
            driver.quit()








