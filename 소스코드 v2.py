import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_yesterday_date():
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime('%Y.%m.%d')

def search_naver_news(keyword, date):
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&pd=3&ds={date}&de={date}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return None
    return response.text

def parse_news(html):
    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.select('ul.list_news > li')
    articles = []

    for news in news_list:
        title_tag = news.select_one('a.news_tit')
        if title_tag:
            title = title_tag.text
            link = title_tag['href']
            press_tag = news.select_one('a.info.press')
            press = press_tag.text if press_tag else ''
            content = get_article_content(link)
            articles.append({
                'title': title,
                'link': link,
                'press': press,
                'content': content,
            })
    return articles

def get_article_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve article content from {url}")
        return ''
    article_html = response.text
    soup = BeautifulSoup(article_html, 'html.parser')
    content = soup.select_one('#articleBodyContents')
    return content.get_text(strip=True) if content else 'Content not found'

def main():
    keyword = 'UAM'
    yesterday = get_yesterday_date()
    html = search_naver_news(keyword, yesterday)
    if html:
        articles = parse_news(html)
        for article in articles:
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}")
            print(f"Press: {article['press']}")
            print(f"Content: {article['content']}")
            print()

if __name__ == "__main__":
    main()
