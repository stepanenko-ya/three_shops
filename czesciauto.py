from selenium import webdriver
import time
from fake_useragent import UserAgent
from proxy import proxy_list
import random
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
import csv
import pickle


ua = UserAgent()


def finder():
    with open("AUTO.csv") as file:
        poland_items = [i.strip('\n').split("|") for i in file.readlines()]
    return poland_items


def writer(res_list):
    with open('result_data.csv', 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        csv_writer.writerow(res_list)


def new_window(iter_items, driver, vendor, brand_name):
    result = []
    for item in iter_items:
        main_window = driver.current_window_handle
        time.sleep(3)
        name = item.find_element_by_class_name("description").find_element_by_class_name("ga-click").text.upper().strip().replace(" ", '')
        vendor_code = item.find_element_by_class_name("description").find_element_by_class_name("nr").text.upper().strip().replace(" ", '')
        if brand_name in name or vendor in vendor_code:
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
                title = driver.find_element_by_class_name("pkw-product__name").find_element_by_tag_name("h2").text.replace(" ", "").upper().strip()
                if vendor == acticle and brand_name in title:
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


def finder_product(items, driver, vendor, brand_name):
    lst = []
    if len(items) == 0:
        lst.extend(["product is out of stock", "0"])
    else:
        iter_items = iter(items)
        funk_result_new_window = new_window(iter_items, driver, vendor, brand_name)
        lst.extend(funk_result_new_window)
    return lst


def czesciauto(list_finder):
    for el in list_finder:
        hunter_list = el[1:3]
        if hunter_list[1] == "Mahle/Knecht":
            new = hunter_list[1].split("/")[1]
            hunter_list[1] = new
        if hunter_list[1] == "KYB (Kayaba)":
            new = hunter_list[1].split(" ")[0]
            hunter_list[1] = new
        if hunter_list[1] == "Lemforder":
            new = "LEMFÖRDER"
            hunter_list[1] = new
        vendor = hunter_list[0].replace(" ", "").upper().strip()
        brand_name = hunter_list[1].replace(" ", "").upper().strip()
        hunter = " ".join(hunter_list)

        x = True
        while x:
            print(hunter)
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={ua.random}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
            options.add_argument("user-data-dir=/home/stepanenko/.config/google-chrome/Default")
            driver = webdriver.Chrome(executable_path="/home/stepanenko/Projects/three_shops/chromedriver",
                                      options=options)
            try:
                driver.get("https://www.czesciauto24.pl/")
                input = driver.find_element_by_id('search')

                input.clear()
                input.send_keys(f'{hunter}')
                driver.implicitly_wait(5)
                input.send_keys(Keys.ENTER)
                items = driver.find_elements_by_class_name('brand-products')
                product_data = finder_product(items, driver, vendor, brand_name)
                if len(product_data) > 0:
                    el.extend(product_data)
                    writer(el)
                else:
                    el.extend(["item not found", "0"])
                    writer(el)
            except Exception as ex:
                print(ex)
            else:
                x = False
            finally:
                driver.close()
                driver.quit()


if __name__ == "__main__":
    list_finders = finder()
    czesciauto(list_finders)









