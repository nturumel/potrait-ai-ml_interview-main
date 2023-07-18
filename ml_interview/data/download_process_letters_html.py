import requests
from bs4 import BeautifulSoup, NavigableString

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


def remove_tables(node):
    if isinstance(node, NavigableString):
        if "......" in node or "------" in node:
            node.extract()
    else:
        for child in node.children:
            remove_tables(child)


def main():
    for year in years:
        create_html(year)


def create_html(year: int):
    url = f"https://www.berkshirehathaway.com/letters/{year}.html"
    response = requests.request("GET", url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    remove_tables(soup)

    with open(f"./ml_interview/data/{year}.html", "w") as f:
        f.write(str(soup))


if __name__ == "__main__":
    main()
