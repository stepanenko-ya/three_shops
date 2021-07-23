import requests
from bs4 import BeautifulSoup
import os




def proxy_parser():
    url = 'https://www.proxyscan.io/home/filterresult?limit=10000&page=1&&status=1&_=1626958080156'
    req = requests.get(url, verify=False)

    file = open("proxy_html", "wb")
    file.write(req.content)
    f_html = open("proxy_html").read()
    soup = BeautifulSoup(f_html, "html.parser")
    trs = soup.find_all("tr")
    proxy_file = open("prox_adress", "w")

    for tr in trs:
        host = tr.find("th").get_text()
        port = tr.find("td").get_text()
        proxy_file.write(f"{host}:{port}\n")
    file.close()
    path = "/home/stepanenko/Projects/three_shops/proxy_html"
    os.remove(path)




