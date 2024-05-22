import requests
from bs4 import BeautifulSoup

def fetch_latest_articles():
    url = 'https://www.aljazeera.com/news/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article', class_='gc u-clickable-card gc--type-post')
        latest_articles = []

        for article in articles[:5]:  # Fetch only the top 5 latest articles
            title = article.find('h3', class_='gc__title').text.strip()
            link = article.find('a', class_='gc__link')['href']
            summary = article.find('p', class_='gc__summary').text.strip()
            latest_articles.append({
                'title': title,
                'link': 'https://www.aljazeera.com' + link,
                'summary': summary
            })

        return latest_articles
    else:
        return None

if __name__ == "__main__":
    articles = fetch_latest_articles()
    if articles:
        for i, article in enumerate(articles, start=1):
            print(f"Article {i}:")
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}")
            print(f"Summary: {article['summary']}")
            print()
    else:
        print("Failed to fetch the latest articles.")
