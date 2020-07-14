# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium import webdriver
from shutil import which

class AtdukeSpider(scrapy.Spider):
    name = 'atDuke'
    allowed_domains = ['www.scholars.duke.edu'] 
    start_urls = [
        'https://www.scholars.duke.edu'
    ]

    def parse(self, response):
        # Making the chrome browser headless, so that it performs the job in the background
        chrome_options = Options()
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36]")

        # Creating a driver out of the chromedriver.exe file. Feeding the driver the appropriate page to start off at.
        driver = webdriver.Chrome(executable_path=r"C:\Users\samar\scraping_Projects\webScraping\scholars\chromedriver", options=chrome_options)
        driver.get("https://scholars.duke.edu/scholars_search/?advanced=true")
        driver.set_window_size(1920, 1080)

        # Use the driver to find the search box and input the desired phrase. After that, press enter and wait 5 seconds to allow the page to load.
        search_input = driver.find_element_by_xpath("(//input[@id ='search'])[1]")
        search_phrase = 'CNN'
        search_input.send_keys(search_phrase)
        search_input.send_keys(Keys.ENTER)
        sleep(5)
        
        # Click on the publications tab, then check off the academic article and conference paper filters
        tab_btn = driver.find_element_by_xpath("//li[@class = 'search-tab']")
        tab_btn.click()
        sleep(5)
        select_academic = driver.find_element_by_xpath(".//*[contains(text(), 'Academic Article')]")
        select_conference = driver.find_element_by_xpath(".//*[contains(text(), 'Conference Paper')]") 

        select_academic.click()
        select_conference.click()
        sleep(1)
        
        next_present = 1
        count = 0
        # while there is a next page, scrape the articles
        while (count < 1):
            currentPage = driver.current_url
            count = count +1

            # creating a resopnse object out of the driver's html
            resp = Selector(text = driver.page_source)
            # find the set of articles and store in "publications"
            publications = resp.xpath("//div[@class = 'col-md-12 col-sm-12']/strong[1]/a[1]")
            # find the next page button and store it in next_page
            next_page = driver.find_element_by_xpath("(//li[@class = 'active'][1]//following::node()[1]//child::node()[1])[1]")
            
            # if the next pag ebutton exists, click on it. Else, set next_present = 0, indicating that the next page doesn't exist.
            if (next_page):               
                next_page.click()
                sleep(1.5)                
            else:
                next_present = 0   

            # iterate through the set of articles
            for publication in publications:
                # For a given article:
                # get the article's link
                link = publication.xpath(".//@href").get()
                # open a new tab, switch to it, and open the article in that new tab.
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                # create a new response object that represents the article's page
                paper_resp = Selector(text=driver.page_source)
                paper = paper_resp.xpath("//section[@id = 'topcontainer']")

                # set default values for the readership stats. If the article doesn't have an altmetric page, the readership stats will remain blank
                citations = " "
                readership = " "
                tweets = " "
                news_mentions = " "

                # attempt to find the altmetric url
                altmetric_url = paper_resp.xpath("//p[@class = 'altmetric-see-more-details']/a/@href").get()
                # if there indeed is an altmetric, proceed to find the article's readership stats
                if(altmetric_url):
                    sleep(1)
                    # using the driver, find the altmetric button and click on it.
                    altmetric_url = driver.find_element_by_xpath("//p[@class = 'altmetric-see-more-details']/a")
                    altmetric_url.click()
                    # create a new resopnse object that represents the altmetric page
                    altmetric_resp = Selector(text=driver.page_source)

                    # set the readership stats to that found in the altmetric page
                    stats = altmetric_resp.xpath("//div[@class = 'score-panel']")
                    citations = stats.xpath(".//div/dl[@class = 'scholarly-citation-counts']/dd/a[contains(text(), 'Dimensions')]/strong[1]/text()").get(),
                    readership = stats.xpath(".//div/h2[contains(text(), 'Readers on')]/following-sibling::dl/dd/a/strong[1]/text()").get(),
                    tweets = stats.xpath(".//div/h2[contains(text(), 'Mentioned by')]/following-sibling::dl/dd/a[contains(text(), ' tweeter')]/strong[1]/text()").get(),
                    news_mentions = stats.xpath(".//div/h2[contains(text(), 'Mentioned by')]/following-sibling::dl/dd/a[contains(text(), ' news outlets')]/strong[1]/text()").get()
                    if not citations:
                        citations = "Not Available"
                    if (stats == ' '):
                        stats = "Not Available"       
                    if type(readership) is tuple:
                        readership = readership[0]
                    if type(tweets) is tuple:
                        tweets = tweets[0]                                     # using the response object we created before (paper_resp), continue scraping the article's main information
                    if type(news_mentions) is tuple:
                        news_mentions = news_mentions[0]
                    if news_mentions is None:
                        news_mentions = "None"
                # find the article's publication location as this can either be represented as plain text or hyperilnk
                pub_loc = paper.xpath(".//*[contains(text(), 'Published In')]/following-sibling::ul/li/a/text()").get()
                if(pub_loc is None):
                    pub_loc = paper.xpath("//*[contains(text(), 'Published In')]/following-sibling::ul/li/text()").get()
                
                # find and output the article's information
                yield{
                    'title': str(paper.xpath(".//section[@id = 'individual-info']/header/h1/text()").get()),
                    'authors': paper.xpath(".//ul[@id = 'individual-DukeAuthors']/following-sibling::ul[1]/li/text()").get(),
                    'published_date': paper.xpath(".//ul[@id = 'individual-PublishedDate']/li[1]/text()").get(),
                    'doi': paper.xpath(".//h3[contains(text(),'Digital Object Identifier (DOI)')]/following-sibling::ul[1]/li/text()").get(),
                    'abstract': paper.xpath(".//div[@class = 'abstract']/p/text()").get(),
                    'publication_location': pub_loc,
                    'link': paper.xpath(".//h3[contains(text(), 'Full Text')]/following-sibling::ul[1]/li[1]/a/@href").get(),
                    'citations': citations,
                    'readership': readership,
                    'tweets': (tweets).replace("\n", ""),
                    'news_mentions': (news_mentions).replace("\n", "")
                }
                
                # close the new tab we created and switch to the main tab that has the set of articles.
                driver.close()
                driver.switch_to.window(driver.window_handles[0])