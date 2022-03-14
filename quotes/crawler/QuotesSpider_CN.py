import requests
from bs4 import BeautifulSoup
import re

URL = "https://baike.baidu.com/item/%E5%90%8D%E4%BA%BA%E5%90%8D%E8%A8%80/383132"
USER_AGENT = "User-Agent: Mozilla/5.0 (X11; Linux x86_64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
SAVE_TO = "quotes_cn.txt"

TITLE_PATTERN = re.compile(r"\s*(名人名言|咟喥咟萪|选自)")
PREFIX_REMOVE_PATTERN = re.compile(r"\s*\d*[.、]\s*")
SUP_NUM_PATTERN = re.compile(r"\s*\[\d*\]")


if __name__ == "__main__":
    print("open file for writing")
    f = open(SAVE_TO, "w")

    print(f"HTTP GET to {URL}")
    response = requests.get(URL, headers={"User-Agent": USER_AGENT})

    print("parsing the response HTML")
    soup = BeautifulSoup(response.text, "lxml")
    divs = soup.find_all("div", attrs={"class": "para"})

    print("remove rubbish")
    for div in divs:
        quote = div.text
        matching = re.match(TITLE_PATTERN, quote)
        if matching:
            continue

        print("+++++++++++++++++++++++++++++++++++++++++")
        print(div.text)
        print("+++++++++++++++++++++++++++++++++++++++++")
        matching = re.match(PREFIX_REMOVE_PATTERN, quote)
        if matching:
            quote = quote[matching.end():]

        quote = re.sub(SUP_NUM_PATTERN, "", quote)

        quote = quote.strip()
        if not quote:
            continue

        f.write(quote)
        f.write("\n")

    f.close()
    print(f"saved result at {SAVE_TO}")
