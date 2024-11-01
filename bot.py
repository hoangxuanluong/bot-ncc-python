from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pytz
import re

vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

load_dotenv()

app = Flask(__name__)
app.config['PORT'] = os.getenv('PORT')

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def fetch_news(url):
    webpage = requests.get(url, headers=HEADERS, proxies={"http": None, "https": None})
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

        publish_time = None
        if time_text:
            specific_time_match = re.search(r'\d{2}/\d{2}/\d{4}', time_text)
            if specific_time_match:
                publish_time = datetime.strptime(specific_time_match.group(), '%d/%m/%Y')
                publish_time = vietnam_timezone.localize(publish_time)
            elif "phút" in time_text:
                minutes = int(time_text.split()[0])
                time_delta = timedelta(minutes=minutes)
                publish_time = datetime.now(vietnam_timezone) - time_delta
            elif "giờ" in time_text:
                hours = int(time_text.split()[0])
                time_delta = timedelta(hours=hours)
                publish_time = datetime.now(vietnam_timezone) - time_delta

        results.append({
            'publishDate': publish_time.strftime('%Y-%m-%d %H:%M:%S') if publish_time else None,
            'url': main_href,
            'title': main_title,
            'source': source_title
        })
    return results[4:]

@app.route('/api/news', methods=['GET'])
def get_news():
    url = request.args.get('url', 'https://baomoi.com/xa-hoi.epi') 
    news_data = fetch_news(url)
    return jsonify(news_data)

@app.route('/', methods=['GET'])
def home():
    return 'luong'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=app.config['PORT'], use_reloader=False)
