from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)
app.config['PORT'] = os.getenv('PORT')

URL = "https://baomoi.com/xa-hoi.epi"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def fetch_news():
    webpage = requests.get(URL, headers=HEADERS, proxies={"http": None, "https": None})
    soup = BeautifulSoup(webpage.content, "html.parser")
    cards = soup.find_all('div', class_='bm-card-content')

    results = []

    for card in cards:
        title_tag = card.find('h3', class_='font-semibold block')
        if title_tag:
            title_a_tag = title_tag.find('a')
            main_href = title_a_tag['href'] if title_a_tag else None
            main_title = title_a_tag['title'] if title_a_tag else None
        else:
            main_href = None
            main_title = None

        source_a_tag = card.find('a', class_='bm-card-source')
        source_title = source_a_tag['title'] if source_a_tag else None

        time_tag = card.find('time', class_='content-time')
        time_text = time_tag.get_text() if time_tag else None

        if time_text:
            if "phút" in time_text:
                minutes = int(time_text.split()[0])
                time_delta = timedelta(minutes=minutes)
            elif "giờ" in time_text:
                hours = int(time_text.split()[0])
                time_delta = timedelta(hours=hours)
            else:
                time_delta = timedelta()

            current_time = datetime.now()
            publish_time = current_time - time_delta
        else:
            publish_time = None

        results.append({
            'publish_time': publish_time.strftime('%Y-%m-%d %H:%M:%S') if publish_time else None,
            'main_href': main_href,
            'main_title': main_title,
            'source_title': source_title
        })

    return results[4:]

@app.route('/api/news', methods=['GET'])
def get_news():
    news_data = fetch_news()
    return jsonify(news_data)

@app.route('/', methods=['GET'])
def home():
    # news_data = fetch_news()
    return 'luong'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=app.config['PORT'], use_reloader=False)
