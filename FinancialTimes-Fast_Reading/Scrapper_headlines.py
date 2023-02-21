import requests
from bs4 import BeautifulSoup

def article_market(number):
    url = "https://www.ft.com/markets"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    article_titles = soup.find_all("a", class_="js-teaser-heading-link")

    titles = []
    for i in range(number):
        combo = []
        x = article_titles[i]
        combo.append(str(x.get_text()))
        combo.append(x['href'])
        titles.append(combo)
    return(titles)