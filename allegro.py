from bs4 import BeautifulSoup
from selenium import webdriver
import time
from fake_useragent import UserAgent
from proxy import proxy_list
from selenium.webdriver.common.action_chains import ActionChains
import random
import pickle
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
from alegro_user import allegro_email, aleeqro_password

ua = UserAgent()


def writer(el):
    with open('allegro.csv', 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        csv_writer.writerow(el)


def reader():
    with open("CZESC.csv") as file:
        poland_items = [i.strip("\n").split("|") for i in file.readlines()]
    return poland_items[269:]


def parsing_items(urls, driver, hunter_lst, vendor_name):
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
        # and vendor_name in ",".join(params_list).upper().replace(" ", '').strip()
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


def beautiful_finder(driver, vebndor_code, vendor_name):
    res = []
    articles = driver.find_element_by_class_name("opbox-listing").find_elements_by_tag_name("article")
    for article in articles:
        title = article.text
        for i in article.find_elements_by_tag_name("dd"):
            title += i.text

        text = title.upper().replace(" ", "").strip()
        if vebndor_code in text and vendor_name in text:
            price = article.find_element_by_class_name("_9c44d_3AMmE").find_element_by_class_name("myre_zn").text.strip(" zł").replace(",", ".")
            item_url = article.find_element_by_class_name("_9c44d_2vTdY").get_attribute("href")
            res.append({"price": float(price),
                        "url": item_url})

    res.sort(key=lambda x: x['price'])
    urls_list = [el["url"] for el in res]

    return urls_list


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

        hunter = " ".join(hunter_list)
        vebndor_code = hunter_list[0].strip().replace(" ", "").upper()
        vendor_name = hunter_list[1].strip().replace(" ", "").upper()
        hunter_lst = []

        hunter_lst.extend([vebndor_code])
        x = True
        while x:
            options_proxy = {
                'proxy': {
                    'https': 'http://xrDNLT:0MK6QA@194.67.215.235:9512',
                }
            }
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={ua.random}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--enable-javascript")
            options.add_argument('--no-sandbox')
            options.add_argument('ignore-certificate-errors')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("user-data-dir=/home/stepanenko/.config/google-chrome/Default")
            options.add_argument("dom.webdriver.enabled")

            driver = webdriver.Chrome(
                executable_path="/home/stepanenko/Projects/three_shops/chromedriver", options=options,
                seleniumwire_options=options_proxy)
            driver.maximize_window()
            try:
                driver.get("https://allegro.pl/")
                pickle.dump(driver.get_cookies(), open(f"{allegro_email}_cookies", "wb"))

                for cookie in pickle.load(open(f"{allegro_email}_cookies", "rb")):
                    driver.add_cookie(cookie)

                time.sleep(random.uniform(4, 29))
                finder_input = driver.find_element_by_tag_name('form').find_element_by_tag_name("input")
                time.sleep(random.uniform(5, 11))
                finder_input.clear()
                finder_input.send_keys(hunter)
                time.sleep(random.uniform(3, 9))
                finder_input.send_keys(Keys.ENTER)
                time.sleep(random.uniform(4, 10))

                urls = beautiful_finder(driver, vebndor_code, vendor_name)
                parsing = parsing_items(urls, driver, hunter_lst, vendor_name)

                if len(parsing) == 0:
                    el.extend(["product is out of stock", "0"])
                else:
                    el.extend(parsing)
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
