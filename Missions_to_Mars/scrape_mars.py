from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
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

    # Featured Image
    # Build query URL for JPL featured [Mars] image - use Splinter to scrape
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Find the image url for the current Featured Mars Image and remove unneeded control text
    featured_image_url = soup.find('article', class_='carousel_item')['style'].\
                        replace('background-image: url(','').\
                        replace(');', '')[1:-1]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url

    # Facts
    # Visit the Mars Facts webpage and use Pandas to scrape the table
    # Three tables returned - use only first table
    results = pd.read_html("https://space-facts.com/mars/")
    facts_df1 = results[0]
    facts_df1.columns = ['Description', 'Mars']
    facts_df1.set_index('Description', inplace=True)
    facts_html1 = facts_df1.to_html()

    # Hemispheres
    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
    # Build query URL for page in USGS Astrogeology site that has pics of Mars' hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find ('div', class_='result-list')
    images = results.find_all('div',{'class':'item'})

    hemisphere_image_urls=[]

    for i in images:
        title = i.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = i.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup=bs(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "mars_facts": facts_html1,
        "hemispheres": hemisphere_image_urls
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_data
