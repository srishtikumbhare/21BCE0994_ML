import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from apscheduler.schedulers.background import BackgroundScheduler
from models import Document

# Database configuration
DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def scrape_news():
    url = "https://news.abplive.com/"  
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract news articles
    articles = soup.find_all('a', class_='storylink') 

    # Save to database
    db = SessionLocal()
    for article in articles:
        title = article.get_text()
        link = article['href']
        content = requests.get(link).text  # Fetch article content
        document = Document(title=title, content=content, user_id='scraper')
        db.add(document)
    db.commit()
    db.close()

def start_scraper():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_news, 'interval', hours=1)  # Run every hour
    scheduler.start()

if __name__ == "__main__":
    start_scraper()
