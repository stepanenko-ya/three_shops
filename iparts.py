from bs4 import BeautifulSoup
from selenium import webdriver
import time
from fake_useragent import UserAgent
from seleniumwire import webdriver
from proxy import proxy_list
import random
from selenium.webdriver.common.keys import Keys
import csv

ua = UserAgent()
URL = "https://www.iparts.pl/znajdz/?idCar=&query="


def reader():
    with open('MA.csv') as file:
        poland_items = [i.split("|") for i in file.readlines()]
    return poland_items


def writer(el):
    with open("IP.csv", "a+",  newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        csv_writer.writerow(el)


def next_page(driver):
    n = None
    try:
        nastepna_button = driver.find_element_by_class_name("button-and-number-pager").find_element_by_link_text("następna >").get_attribute("href")
    except:
        n = "last page"
    else:
        time.sleep(2)
        next_page = nastepna_button.split("page=")[1]
        if int(next_page) <= 2:
            n = nastepna_button
        else:
            n = "last page"
    finally:
        return n


def new_window(iter_items, driver, vendor, hunter_list):
    result = []
    for item in iter_items:
        time.sleep(random.uniform(4, 14))
        name_item = item.find_element_by_class_name("nazwa").find_element_by_tag_name("a").text.replace(" ", "").strip().upper()
        hunter_name = hunter_list[1].upper().replace(" ", '')
        if vendor.upper() in name_item and hunter_name in name_item:
            main_window = driver.current_window_handle
            link = item.find_element_by_class_name("nazwa").find_element_by_tag_name("a").get_attribute("href")
            time.sleep(random.uniform(2, 9))
            driver.execute_script("window.open();")
            driver.switch_to_window(driver.window_handles[1])
            driver.get(link)
            time.sleep(random.uniform(3, 10))
            trademark = driver.find_element_by_css_selector('span[itemprop="brand"]').text.replace(" ", "").upper()
            vendor_item = driver.find_element_by_css_selector('span[itemprop="mpn"]').text.replace(" ", "").upper()
            if vendor.upper() == vendor_item and hunter_name in trademark:
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
            if vendor.upper() in name_item or hunter_name in name_item:
                main_window = driver.current_window_handle
                link = item.find_element_by_class_name("nazwa").find_element_by_tag_name("a").get_attribute("href")
                time.sleep(4)
                driver.execute_script("window.open();")
                driver.switch_to_window(driver.window_handles[1])
                driver.get(link)
                time.sleep(4)
                trademark = driver.find_element_by_css_selector('span[itemprop="brand"]').text.replace(" ", "").upper()
                vendor_item = driver.find_element_by_css_selector('span[itemprop="mpn"]').text.replace(" ", "").upper()
                if vendor.upper() == vendor_item and hunter_name in trademark:
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
    lst = []
    if len(items) == 0:
        lst.append("product not found")
        lst.append("0")
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
        vendor = hunter_list[0].replace(" ", "")
        hunter_derty = " ".join(hunter_list)
        hunter = hunter_derty.replace(" ", "+").replace("/", "%")
        finder_url = URL + hunter

        del el[6:]

        x = True
        while x:
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={ua.random}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument('--no-sandbox')
            options.add_argument('ignore-certificate-errors')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("user-data-dir=/home/stepanenko/.config/google-chrome/Default")
            options.add_argument("dom.webdriver.enabled")
            # options.add_argument("--headless")
            options_proxy = {
                'proxy': {
                    'https': 'http://xrDNLT:0MK6QA@194.67.215.235:9512',
                }
            }
            driver = webdriver.Chrome(executable_path="/home/stepanenko/Projects/three_shops/chromedriver",
                                      options=options,  seleniumwire_options=options_proxy)

            try:
                pagination = True
                while pagination:
                    driver.get(finder_url)
                    time.sleep(3)
                    items = driver.find_element_by_id('SklepKatalog').find_elements_by_class_name("produkt")

                    product_data = finder_product(items, driver, vendor, hunter_list)
                    if len(product_data) > 0:
                        el.append("|".join(product_data))
                        writer(el)
                        pagination = False

                    else:
                        next__page = next_page(driver)
                        if next__page != "last page":
                            finder_url = next__page
                        else:
                            el.append("item not found")
                            pagination = False
                            el.append("0")
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
