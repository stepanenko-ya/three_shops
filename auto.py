from bs4 import BeautifulSoup
from selenium import webdriver
import time
from fake_useragent import UserAgent
# from seleniumwire import webdriver
import pickle

import random
from selenium.webdriver.common.keys import Keys
import csv
import json

ua = UserAgent()


def writer(el):
    with open('p.csv', 'a+',  newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        csv_writer.writerow(el)


def reader():
    with open("MA.csv") as file:
        poland_items = [i.split("|") for i in file.readlines()]
    return poland_items


def new_window(iter_items, driver, vendor, hunter_list):
    trademark = hunter_list[1].upper().replace(" ", "").strip()
    result = []
    time.sleep(random.uniform(6, 12))
    main_window = driver.current_window_handle
    for item in iter_items:
        vendor_code = item.find_element_by_class_name("article_number").text.split("Numer artykułu: ")[1].upper().replace(" ", "").strip()
        name_item = item.find_element_by_class_name("name").text.upper().replace(" ", "").strip()

        if trademark in name_item or vendor in vendor_code:
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
                print(title)
                art = driver.find_element_by_class_name("subtitle-art-nummer").text.split("Numer artykułu:")[1].strip().upper().replace(" ", '')
                if vendor == art and trademark in title:
                    try:
                        price = driver.find_element_by_class_name('product-new-price').text.split(" ")[0]
                    except:
                        price = "0"
                    result.extend([driver.current_url, price])
                    break
                driver.close()
                driver.switch_to_window(main_window)
    return result


def finder_product(items, driver, vendor, hunter_list):
    lst = []
    if len(items) == 0:
        lst.extend(["product is out of stock", "0"])
    else:
        iter_items = iter(items)
        funk_result_new_window = new_window(iter_items, driver, vendor, hunter_list)
        lst.extend(funk_result_new_window)
    return lst


def main(reading):

    for el in reading:
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
        TM_name = hunter_list[1].replace(" ", "").upper().strip()
        hunter = " ".join(hunter_list)
        print(vendor)
        finder_url = f"https://www.autodoc.pl/search?keyword={vendor}+{TM_name}"
        x = True
        while x:
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
            options.add_argument(f"--proxy-server={random.choice(proxy_list)}")
            options.add_argument("dom.webdriver.enabled")
            # options.add_argument("user-data-dir=selenium")
            # options.add_argument("--remote - debugging - port = 9222")
            options.add_argument("--disable - blink - features = AutomationControlle")
            options.add_argument("user-data-dir=/home/stepanenko/.config/google-chrome/Default")
            driver = webdriver.Chrome(executable_path="/home/stepanenko/Projects/three_shops/chromedriver",
                                      options=options)

            try:
                with open('cookietest.json', 'r', newline='') as inputdata:
                    cookies = json.load(inputdata)
                driver.get(finder_url)
                for i in cookies:
                    driver.add_cookie(i)


                # driver.get("https://stackoverflow.com/")
                # cookies = driver.get_cookies()
                # with open('cookietest.json', 'w', newline='') as outputdata:
                #     json.dump(cookies, outputdata)
                #
                # print('send cookie')


                # cooks = driver.get_cookies()

                # input = driver.find_element_by_id('search')
                # input.clear()
                # input.send_keys(hunter)
                # time.sleep(random.uniform(2, 20))
                # driver.find_element_by_link_text("Szukaj")


                # time.sleep(random.uniform(5, 20))
                # input = driver.find_element_by_id('search')
                # input.clear()
                # input.send_keys(hunter)
                # time.sleep(random.uniform(2, 7))
                # input.send_keys(Keys.ENTER)
                # time.sleep(random.uniform(2, 9))
                time.sleep(random.uniform(30, 60))
                items = driver.find_element_by_class_name("js-listing-wrap").find_elements_by_class_name('description')


                product_data = finder_product(items, driver, vendor, hunter_list)
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
    reading = reader()
    main(reading)

