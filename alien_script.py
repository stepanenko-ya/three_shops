from selenium import webdriver
from time import sleep
from PIL import Image


class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="/home/stepanenko/Projects/three_shops/geckodriver")
        self.navigate()

    def screen_short(self):
        self.driver.save_screenshot("avito.png")

    def crop(self):
        pass

    def navigate(self):
        self.driver.get("https://www.avito.ru/moskva/telefony/iphone_7_2156915436")
        "styles-item-phone-button_height-3SOiy button-button-2Fo5k button-size-l-3LVJf button-success-1Tf-u width-width-12-2VZLz"
        button = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/span/span/button")
        button.click()
        self.screen_short()
        sleep(6)
        image = self.driver.find_element_by_class_name("contacts-phone-3KtSI")
        location = image.location
        size = image.size
        self.driver.close()
        self.crop(location, size)


def main():
    b = Bot()


if __name__ == "__main__":
    main()
