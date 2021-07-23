from selenium import webdriver
import time
from fake_useragent import UserAgent
import random
import json
from selenium.webdriver.common.keys import Keys
import pickle


ua = UserAgent()


def new_window(driver):
    main_window = driver.current_window_handle
    time.sleep(3)
    url = driver.find_element_by_id("header-links").find_elements_by_tag_name("li")[1].find_element_by_tag_name("a").get_attribute("href")
    print(url)
    driver.execute_script("window.open();")
    driver.switch_to_window(driver.window_handles[1])
    driver.get(url)
    time.sleep(20)
    driver.close()
    driver.switch_to_window(main_window)


def finder_product(driver):
    funk_result_new_window = new_window(driver)
    lst = funk_result_new_window
    return lst


def my_ip():
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
            driver.get("https://proxy6.net/en/privacy")
            with open("czesc_cookies", 'w') as filehandler:
                json.dump(driver.get_cookies(), filehandler)

            with open("czesc_cookies", 'r') as cookiesfile:
                cookies = json.load(cookiesfile)
            for cookie in cookies:
                print(cookie)
                driver.add_cookie(cookie)
            time.sleep(random.uniform(9, 30))
            product_data = finder_product(driver)

        except Exception as ex:
            print(ex)
        else:
            x = False
            return product_data
        finally:
            driver.close()
            driver.quit()
