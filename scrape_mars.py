#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path":"chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_facts_data = {}

    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(2)

    html = browser.html
    soup = bs(html,"html.parser")

    #scrapping latest news about mars from nasa
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    facts_data['news_title'] = news_title
    facts_data['news_p'] = news_p
    
    #Mars Featured Image
    nasa_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(nasa_image)
    time.sleep(2)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(nasa_image))
    
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    time.sleep(2)
    
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = base_url + img_url
    facts_data["featured_image"] = full_img_url
    
    #Mars Weather

    #get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    facts_data["mars_weather"] = mars_weather

    #Mars Facts

    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)
    table = pd.read_html(url_facts)
    table[0]

    df_facts = table[0]
    df_facts.columns = ["Parameter", "Values"]
    clean_table = df_facts.set_index(["Parameter"])
    html_table = clean_table.to_html()
    html_table = html_table.replace("\n", "")
    facts_data["mars_facts_table"] = html_table

    return facts_data
