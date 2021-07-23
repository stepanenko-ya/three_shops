import time
from fake_useragent import UserAgent
from selenium import webdriver
import random


ua = UserAgent()


def new_window(iter_items, driver, vendor_name, vendor_code):
    result = []
    for item in iter_items:
        time.sleep(random.uniform(4, 14))
        name_item = item.find_element_by_class_name("nazwa").find_element_by_tag_name("a").text.replace(" ", "").strip().upper()
        vendor_code = vendor_code.upper().replace(" ", '')
        if vendor_name.upper().replace(" ", "") in name_item and vendor_code in name_item:
            main_window = driver.current_window_handle
            link = item.find_element_by_class_name("nazwa").find_element_by_tag_name("a").get_attribute("href")
            time.sleep(random.uniform(2, 9))
            driver.execute_script("window.open();")
            driver.switch_to_window(driver.window_handles[1])
            driver.get(link)
            time.sleep(random.uniform(3, 10))
            trademark = driver.find_element_by_css_selector('span[itemprop="brand"]').text.replace(" ", "").upper()
            vendor_item = driver.find_element_by_css_selector('span[itemprop="mpn"]').text.replace(" ", "").upper()
            if vendor_code == vendor_item and vendor_name.upper().replace(" ", '') in trademark:
                result.append(driver.current_url)
                try:
                    price = driver.find_element_by_css_selector('span[itemprop="price"]').text
                except:
                    price = "0"
                result.append(price)
                break
            else:
                driver.close()
                driver.switch_to_window(main_window)
        else:
            if vendor_name.upper() in name_item or vendor_code in name_item:
                main_window = driver.current_window_handle
                link = item.find_element_by_class_name("nazwa").find_element_by_tag_name("a").get_attribute("href")
                time.sleep(4)
                driver.execute_script("window.open();")
                driver.switch_to_window(driver.window_handles[1])
                driver.get(link)
                time.sleep(4)
                trademark = driver.find_element_by_css_selector('span[itemprop="brand"]').text.replace(" ", "").upper()
                vendor_item = driver.find_element_by_css_selector('span[itemprop="mpn"]').text.replace(" ", "").upper()
                if vendor_code == vendor_item and vendor_name.upper() in trademark:
                    result.append(driver.current_url)
                    try:
                        price = driver.find_element_by_css_selector('span[itemprop="price"]').text
                    except:
                        price = "0"
                    result.append(price)
                    break
                else:
                    driver.close()
                    driver.switch_to_window(main_window)
    return result


def finder_product(items, driver, vendor, hunter_list):
    if len(items) == 0:
        lst = ["product not found", "0"]
    else:
        iter_items = iter(items)
        funk_result_new_window = new_window(iter_items, driver, vendor, hunter_list)
        lst = funk_result_new_window
    return lst


def iparts(vendor_name, vendor_code):
    x = True
    hunter_derty = f"{vendor_code.replace(' ', '+')} {vendor_name}"
    hunter = hunter_derty.replace(" ", "+").replace("/", "%")
    finder_url = "https://www.iparts.pl/znajdz/?idCar=&query=" + hunter
    print(finder_url)

    while x:
        proxy_list = open("prox_adress").read().split("\n")
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=socks4://' + random.choice(proxy_list))
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-javascript")
        options.add_argument('--no-sandbox')
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("dom.webdriver.enabled")
        driver = webdriver.Chrome(executable_path="/home/stepanenko/Projects/three_shops/chromedriver",
                                  options=options)
        try:
            driver.get(finder_url)
            my_cookies = driver.get_cookies()
            for my_cook in my_cookies:
                driver.add_cookie(my_cook)
            time.sleep(random.uniform(5, 15))
            items = driver.find_element_by_id('SklepKatalog').find_elements_by_class_name("produkt")
            product_data = finder_product(items, driver, vendor_name, vendor_code)

        except Exception as ex:
            print(ex)
        else:
            x = False
            return product_data

        finally:
            driver.close()
            driver.quit()

