import requests
from bs4 import BeautifulSoup
import re
import json

URL = "https://blog.hubspot.com/sales/famous-quotes"
USER_AGENT = "User-Agent: Mozilla/5.0 (X11; Linux x86_64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
SAVE_TO = "quotes_en.txt"

PREFIX_REMOVE_PATTERN = re.compile(r'\s*\d*[.、]\s*')
SUP_PATTERN = re.compile(r'["\\]')



if __name__ == "__main__":
    print("open file for writing")
    f = open(SAVE_TO, "w")

    print(f"HTTP GET to {URL}")
    response = requests.get(URL, headers={"User-Agent": USER_AGENT})

    print("parsing the response HTML")
    soup = BeautifulSoup(response.text, "lxml")
    divs = soup.find(attrs={"id": "hs_cos_wrapper_post_body"}).find_all("p")

    print("remove rubbish")
    for div in divs:
        quote = div.text

        matching = re.match(PREFIX_REMOVE_PATTERN, quote)
        if matching:
            quote = quote[matching.end():]
        else:
            continue

        quote = re.sub(SUP_PATTERN, "", quote)
        quote = quote.strip()

        f.write(quote)
        f.write("\n")

    f.close()
    print(f"saved result at {SAVE_TO}")
