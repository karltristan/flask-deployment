from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

URL = [
    "https://hollowknight.fandom.com/wiki/Hollow_Knight:_Silksong",
    "https://www.teamcherry.com.au/about",
    "https://k4g.com/blog/platformer-games/gamers-most-wanted-premieres-hollow-knight-silksong#4",
]

target_url_1 = "https://hollowknight.fandom.com/wiki/Hollow_Knight:_Silksong"
target_url_2 = "https://www.teamcherry.com.au/about"
target_url_3 = "https://k4g.com/blog/platformer-games/gamers-most-wanted-premieres-hollow-knight-silksong#4"

def scrape_data():
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    for url in URL:
        if url == target_url_1:
            scrape = requests.get(url, headers=headers)
            soup = BeautifulSoup(scrape.text, "html.parser")
            title = soup.find("span", attrs={"class": "mw-page-title-main"})
            data["title"] = title.text if title else "Not Found"


    for url in URL:
        if url == target_url_3:
            scrape = requests.get(url, headers=headers)
            soup = BeautifulSoup(scrape.text, "html.parser")
            paragraphs = soup.find_all("p")
            target_text = " to be available on multiple platforms"
            platforms = [p.text for p in paragraphs if target_text in p.text]
            data["platforms"] = platforms[0] if platforms else "Not Found"


    for url in URL:
        if url == target_url_1:
            scrape = requests.get(url, headers=headers)
            soup = BeautifulSoup(scrape.text, "html.parser")
            developers = soup.find("a", attrs={"title": "Team Cherry"})
            data["developer"] = developers.text if developers else "Not Found"


    for url in URL:
        if url == target_url_2:
            scrape = requests.get(url, headers=headers)
            soup = BeautifulSoup(scrape.text, "html.parser")
            pub_info = soup.find("div", attrs={"class": "sqs-html-content"})
            data["publisher"] = pub_info.text.replace("THE TEAM", "").strip() if pub_info else "Not Found"

    # Scrape Key Features
    for url in URL:
        if url == target_url_3:
            scrape = requests.get(url, headers=headers)
            soup = BeautifulSoup(scrape.text, "html.parser")
            ol = soup.find("ol")
            key_features = [li.text.strip() for li in ol.find_all("li")] if ol else ["Not Found"]
            data["features"] = key_features

    # Scrape Release Date Info
    for url in URL:
        if url == target_url_3:
            scrape = requests.get(url, headers=headers)
            soup = BeautifulSoup(scrape.text, "html.parser")
            paragraphs = soup.find_all("p")
            target_text = "There is no official release"
            release_date_info = [p.text for p in paragraphs if target_text in p.text]
            data["release_date"] = release_date_info[0] if release_date_info else "Not Found"

    return data

@app.route("/")
def home():
    data = scrape_data()
    return render_template("index.html", data=data)
if __name__ == "__main__":
    app.run(debug=False)
