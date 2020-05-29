
#Import libraries
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def scrape():
    mars_dict = {}
    ######### start splinter in OSX #########
    def init_browser():
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        return Browser("chrome", **executable_path, headless = False)
    browser=init_browser()
    ########## Scrape Mars news page #############
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(2)
    html = browser.html
    #Take the html into a soup object
    soup = bs(html,"html.parser")

    marsnews={}
    #Take the first title you find
    titulo = soup.find("div",class_="list_text").a.text
    #Take the firs article teaser you find
    parafo = soup.find("div", class_="article_teaser_body").text
    #add them into marsnews dict
    marsnews['titulo'] = titulo
    marsnews['parafo'] = parafo

    mars_dict["last_news"] = marsnews

    ########### GET MARS LAST IMAGE ########
    nasa_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa_img)
    time.sleep(2)
    html = browser.html
    #new soup
    soup = bs(html,"html.parser")
    #Search for the link
    img_link = soup.find("section", class_="grid_gallery module grid_view").ul.li.a["data-fancybox-href"]
    #The given link was incomplete so... 
    #I found this requests function that allows to join an absolute path to the relative path within 
    img_link = requests.compat.urljoin(nasa_img, img_link)

    mars_dict["last_image"] = img_link

    ####### GET MARS WEATHER ###########
    #New browser visit
    nasa_twitt = "https://twitter.com/marswxreport?lang=en"
    browser.visit(nasa_twitt)
    time.sleep(2)
    html = browser.html
    #New soup
    soup = bs(html, "html.parser")
    #get the right tweet
    #So first we have to take all the tweets
    tweets = soup.main.section.div.find_all("div", {"data-testid" : "tweet"})

    #Then we iterate through tweets 
    for tweet in tweets:
        # Make sure the tweet is from Mars Weather
        author = tweet.span.string
        if author == "Mars Weather":
            #If it is, take the text of the tweet
            mars_weather = tweet.find("div", {"lang":"en"}).span.string.strip()
            #Stop iterate
            break
    mars_dict["weather"] = mars_weather

    ######### GET MARS FACTS IN A TABLE ##############
    facts_page = "https://space-facts.com/mars/"
    browser.visit(facts_page)
    time.sleep(2)
    html = browser.html
    #Soup
    soup = bs(html, "html.parser")
    #to make posible to pandas to read a soup element i had to transform the string into a prettify
    table_loc = soup.section.article.find("div", id="text-75").table.prettify()
    #now we can use "read_html" from pandas
    table = pd.read_html(table_loc)
    #But to use it for our next page we have to convert it again into html
    #First I transform to a DataFrame
    table = pd.DataFrame(table[0])
    #And then to a html, without index and header
    table = table.to_html(index=False, header=False )

    mars_dict["facts_table"] = table

    ######## GET HEMISPHERE IMAGES FROM MARS ############
    hemispage = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispage)
    time.sleep(2)
    html = browser.html
    #Soup
    soup = bs(html, "html.parser")
    hemisphere_image_url = [] 
    #First we get in a list the four parts with the different hemispheres 
    hemispheres = soup.section.find("div", class_="collapsible results").find_all("div", class_="item")

    #Then we iterate through the hemispheres
    for x in hemispheres:
        #Take the href link to the page who has the image and complete it
        link = x.a["href"]
        link = requests.compat.urljoin(hemispage, link)
        #Visit the new page
        browser.visit(link)
        time.sleep(2)
        # Read the html of the new page
        html = browser.html
        soup = bs(html, "html.parser")
        #Get the title and the links to image and put them in a dictionary
        title = soup.section.h2.string.replace("Enhanced", "")
        links = soup.div.ul.li.a["href"]
        dictionary = {"title" : title , "img_link" : links }
        #apend the dictionary to the list of urls
        hemisphere_image_url.append(dictionary)
        #Get back to the original page
        browser.back()
    
    mars_dict["hemispheres_img"] = dictionary

    return mars_dict


  
            




    

   