# Import Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time

def scrape():
    mars_dict = {}
    # Mars News Title
    # ===========================

    # Get the URL to be scraped
    mars_news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2019%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Create Splinter Browser Instance
    browser = Browser('chrome')
    browser.visit(mars_news_url)

    mars_news_html = browser.html
    mars_news_soup = BeautifulSoup(mars_news_html, 'html5lib')

    # Close the browser
    print(f'Latest Mars News Title: {mars_news_soup}')
    browser.quit()


    # Capture the Latest Mars News Title
    print(mars_news_soup.find("h3"))
    mars_dict['mnews_title'] = mars_news_soup.find("h3").text

    # Capture the Latest Mars News Paragraph Text
    mars_dict['mnews_pgraph'] = mars_news_soup.find("div", class_="article_teaser_body").text
    




    # JPL Featured Image
    # ==========================


    # Use Splinter to find JPL Featured Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Create Spliner Browser Instance
    jpl_browser = Browser('chrome')

    # Visit JPL Mars Images page
    jpl_browser.visit(jpl_url)

    # Click the JPL Featured Image 'Full Image' button (link)
    jpl_browser.click_link_by_id('full_image')

    # Allow the page to load completely
    time.sleep(2)

    # Click on the 'More Info' button (link) in order to get to Large Image
    jpl_browser.click_link_by_partial_href('/spaceimages/details.php')

    # Allow the page to load completely
    time.sleep(2)

    # Get Large Image HTML & Parse
    jpl_lg_img_html = jpl_browser.html
    jpl_lg_img_soup = BeautifulSoup(jpl_lg_img_html, 'html5lib')

    # Capture JPL Large Featured Image
    mars_dict['jpl_img_lg_url'] = "https://www.jpl.nasa.gov" + jpl_lg_img_soup.find("img",class_="main_image")['src']

    # Close the Browser
    jpl_browser.quit()



    # Mars Weather
    # =======================

    # Use Splinter to find Mars Weather Info
    mars_weather_feed = "https://twitter.com/marswxreport?lang=en"

    # Navigate to the Mars Weather Twitter Feed
    twitter_browser = Browser('chrome')
    twitter_browser.visit(mars_weather_feed)

    # Scrape the Mars Weather Feed & Parse
    mars_weather_feed_html = twitter_browser.html
    mars_weather_feed_soup = BeautifulSoup(mars_weather_feed_html,'html5lib')

    # Capture the Latest Mars Weather Report
    mars_dict['mars_weather'] = mars_weather_feed_soup.find("div", class_="js-tweet-text-container").find('p').text.replace("\n"," ")

    # Close Browser
    twitter_browser.quit()




    # Mars Facts
    # =====================

    # Import Pandas
    import pandas as pd

    # Define the URL 
    mars_facts_url = "https://space-facts.com/mars/"

    # Use Pandas to scrape the Mars Facts page for tables
    mars_facts_tables = pd.read_html(mars_facts_url)

    # Convert Scraped HTML to a DataFrame, rename the columns, and set the index
    mars_facts_df = mars_facts_tables[0]
    mars_facts_df = mars_facts_df.rename(columns= {0:'Category',1:'Value'})
    mars_facts_df = mars_facts_df.set_index('Category')

    # Convert DataFrame to HTML table string
    mars_facts_html_table = mars_facts_df.to_html()
    mars_facts_html_table

    # Strip Unwanted characters
    mars_facts_html_table.replace("\n","")

    # Save the HTML table to a file
    mars_facts_df.to_html('mars_facts_table.html')



    # Mars Hemispheres
    # ===========================

    # Store the USGS Astrogeology Mars Hemisphere site's url
    mars_hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Scrape the Page for the HTML
    hemi_browser = Browser('chrome')

    # Visit the USGS Astrogeology site
    hemi_browser.visit(mars_hemi_url)

    # Scrape the site and parse
    mars_hemi_html = hemi_browser.html
    mars_hemi_soup = BeautifulSoup(mars_hemi_html, 'html5lib')

    # Find all the image tags with class 'thumb'
    hemi_link_list = mars_hemi_soup.find_all("a", class_="itemLink product-item")

    # Remove duplicates from list
    hemi_link_list = hemi_link_list[::2]

    # Make a new list of all image urls
    new_url_list = []
    base_url = "https://astrogeology.usgs.gov"
    for link in hemi_link_list:
        new_url_list.append(base_url + link.get('href'))

    # Scrape the full resolution image & title from each url and add it to a dictionary
    full_img_list = []
    for url in new_url_list:
        hemi_browser.visit(url)
        full_img_html = hemi_browser.html
        full_img_soup = BeautifulSoup(full_img_html, 'html5lib')
        full_img_url = full_img_soup.find("a", target="_blank").get('href')
        full_img_title = full_img_soup.find("h2", class_='title').text.replace('Enhanced',"").rstrip()
        
        full_img_list.append({'title': full_img_title, 'img_url': full_img_url})
        
    # Close the browser
    hemi_browser.quit()
    mars_dict['full_img_list'] = full_img_list 

    return mars_dict

scrape()


