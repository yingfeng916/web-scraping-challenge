import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('div', class_="list_text")
    
    news_title = results.find('div', class_='content_title').text
    news_p = results.find('div', class_='article_teaser_body').text

    
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    html_2 = browser.html
    soup_2 = BeautifulSoup(html_2, 'html.parser')
    article = soup.article
    results_2 = soup_2.find('figure', class_='lede')
    featured_image_url = f"https://www.jpl.nasa.gov/{results_2.a['href']}"
   

    url_3 = "https://space-facts.com/mars/"
    tables = pd.read_html(url_3)
    df = tables[0]
    html_table = df.to_html()
    
    
    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)

    hemisphere_image_urls = []

    html_4 = browser.html
    soup_4 = BeautifulSoup(html_4, 'html.parser')

    sections = soup_4.find_all('div', class_='description')

    for section in sections:
        d1 = {}
        title = section.find('h3').text.strip()
        d1['title'] = title
        browser.click_link_by_partial_text(title)

        html_5 = browser.html
        soup_5 = BeautifulSoup(html_5, 'html.parser')

        grab = soup_5.find('img', class_='wide-image')
        img_url = f"https://astrogeology.usgs.gov/{grab['src']}"
        d1['img_url'] = img_url

        hemisphere_image_urls.append(d1)
        browser.back()
        
        data = {"news_title":news_title, "news_paragraph":news_p, "featured_image":featured_image_url, "facts_table":html_table, "hemispheres":hemisphere_image_urls}

    return data
        
    