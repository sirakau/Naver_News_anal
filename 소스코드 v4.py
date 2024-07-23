import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def get_yesterday_date():
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime('%Y.%m.%d')

def search_naver_news(keyword, date):
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&pd=3&ds={date}&de={date}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return None
    return response.text

def extract_news_links(html):
    # Using regular expression to find all n.news.naver.com links
    links = re.findall(r'https://n.news.naver.com/[^"]+', html)
    return list(set(links))  # Remove duplicates by converting to set and back to list

def get_article_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        print(f"Failed to retrieve article content from {url}")
        return '', ''
    article_html = response.text
    soup = BeautifulSoup(article_html, 'html.parser')
    # Extract the title and content based on the current structure of Naver News
    title = soup.select_one('h2.media_end_head_headline')  # Example selector for Naver News article title
    content = soup.select_one('article#dic_area')  # Example selector for Naver News article content
    title_text = title.get_text(strip=True) if title else 'Title not found'
    content_text = content.get_text(strip=True) if content else 'Content not found'
    return title_text, content_text

def main():
    keyword = 'UAM'
    yesterday = get_yesterday_date()
    html = search_naver_news(keyword, yesterday)
    if html:
        links = extract_news_links(html)
        for link in links:
            title, content = get_article_content(link)
            print(f"Title: {title}")
            print(f"Link: {link}")
            print(f"Content: {content}")
            print()

if __name__ == "__main__":
    main()
