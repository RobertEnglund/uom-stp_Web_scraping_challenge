from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # NASA Mars News
    # Collect the latest News Title and Paragraph Text
    # Assign the text to variables that you can reference later
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
#    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find('div', class_='bottom_gradient').text
    news_p = soup.find('div', class_='article_teaser_body').text



    # Store data in a dictionary
    mars_data = {
#        "sloth_img": sloth_img,
        "news_title": news_title,
        "news_p": news_p
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_data
