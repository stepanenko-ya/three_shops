import csv
import random
import time
from proxy_parsing import proxy_parser
from iparts_main import iparts
from czens_main import czesciauto
from autodoc_main import autodoc
from allegro_main import allegro



def writer(el):
    with open('fff.csv', 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='$')
        csv_writer.writerow(el)


def main(urls):
    proxy_parser()
    # proxy_list = open("prox_adress").read().split("\n")
    columns_title = ["Ware ID$Артикул", "Марка (бренд)", "Номенклатура, Ед. изм.",
                     "https://2407.pl/$https://www.iparts.pl/", "price",
                     "https://www.czesciauto24.pl/", "price",
                     "https://www.autodoc.pl/", "price",
                     "https://allegro.pl/", "price"]
    # writer(columns_title)
    for el in urls[3:]:
        # time.sleep(random.uniform(15, 28))
        del el[5:]
        vendor_code = el[1]
        vendor_name = el[2]
        if vendor_name == "Mahle/Knecht":
           vendor_name = vendor_name.split("/")[1]
        if vendor_name == "KYB (Kayaba)":
            vendor_name = vendor_name.split(" ")[0]
        if vendor_name == "Lemforder":
            vendor_name = "LEMFÖRDER"
        # el.extend(iparts(vendor_name, vendor_code))
        # el.extend(czesciauto(vendor_name, vendor_code))
        # el.extend(autodoc(proxy_list, vendor_name, vendor_code))
        # el.extend(allegro(proxy_list, vendor_name, vendor_code))
        # allegro(proxy_list, vendor_name, vendor_code)
        # print(el)

        # writer(el)


if __name__ == "__main__":
    urls = [i.split("$") for i in open("URLS_POLAND.csv").readlines()]
    main(urls)
