import csv
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

# years = [1983, 1984, 1985, 1986, 1987, 1988]
years = [*range(1983, 1989)]
print(years)

payload = ""
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.berkshirehathaway.com/letters/letters.html",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}


def main():
    for year in years:
        create_csv(year)


def create_csv(year: int):
    url = f"https://www.berkshirehathaway.com/letters/{year}.html"
    response = requests.request("GET", url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    pre = soup.find("pre")
    for _b in pre.find_all("b"):
        if str(_b) == "<b>o</b>":
            _b.decompose()

    broken_pre = re.split("(<b>.+[\n]?<\/b>)", str(pre))[1:]

    f = open(f"./ml_interview/data/{year}.csv", "w")
    writer = csv.writer(f)
    section = ""
    for document_section in broken_pre:
        if "<b>" in document_section:  # Unused
            section = document_section.replace("<b>", "").replace("</b>", "")
            section = section.replace("\r\n", "").strip().lower()
            section = section.replace(
                "see\x92s candy shops, inc.", "see\x92s candy shops"
            )
            continue
        for subsection in document_section.split("\r\n\r\n"):
            if "......" in subsection or "------" in subsection:
                # we don't want the tables
                continue
            if subsection == "":
                continue
            subsection = subsection.replace("\r\n", "").strip()
            writer.writerow([str(subsection)])

    f.close()
