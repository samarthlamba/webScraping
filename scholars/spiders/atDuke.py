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
        chrome_options = Options()
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36]")

        driver = webdriver.Chrome(executable_path=r"C:\Users\samar\scraping_Projects\scholars\scholars\chromedriver", options=chrome_options)
        driver.get("https://scholars.duke.edu/scholars_search/?advanced=true")
        driver.set_window_size(1920, 1080)

        search_input = driver.find_element_by_xpath("(//input[@id ='search'])[1]")
        search_input.send_keys('Machine Learning')

        search_input.send_keys(Keys.ENTER)
        sleep(5)
        
        driver.save_screenshot("initialarticlepage.png")
        tab_btn = driver.find_element_by_xpath("//li[@class = 'search-tab']")
        tab_btn.click()
        sleep(5)
        
        driver.save_screenshot("initialarticlepage.png")
        select_academic = driver.find_element_by_xpath(".//*[contains(text(), 'Academic Article')]") #type_AcademicArticle
        select_conference = driver.find_element_by_xpath(".//*[contains(text(), 'Conference Paper')]") 

        select_academic.click()
        select_conference.click()
        sleep(1)
        
        next_present = 1
        count = 0
        while (count < 1):
            currentPage = driver.current_url
            count = count +1
            resp = Selector(text = driver.page_source)
            publications = resp.xpath("//div[@class = 'col-md-12 col-sm-12']/strong[1]/a[1]")
            next_page = driver.find_element_by_xpath("(//li[@class = 'active'][1]//following::node()[1]//child::node()[1])[1]")
            
            print('hello')
            if (next_page):         
                                
                next_page.click()
                sleep(1.5)
                
                driver.save_screenshot("nextpage.png") 
            else:
                next_present = 0   

            for publication in publications:
                print("hellllllllllllllllllllllllllo")
                link = publication.xpath(".//@href").get()
                
                driver.save_screenshot("initialarticlepage.png")
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                driver.save_screenshot("newtab.png")
                paper_resp = Selector(text=driver.page_source)
                paper = paper_resp.xpath("//section[@id = 'topcontainer']")

                citations = " "
                readership = " "
                tweets = " "
                news_mentions = " "

                # if there is an altmetric, set the score values
                print(driver.page_source)
                altmetric_url = paper_resp.xpath("//p[@class = 'altmetric-see-more-details']/a/@href").get()
                if(altmetric_url):
                    sleep(1)
                    altmetric_url = driver.find_element_by_xpath("//p[@class = 'altmetric-see-more-details']/a")
                    altmetric_url.click()
                    altmetric_resp = Selector(text=driver.page_source)
                    stats = altmetric_resp.xpath("//div[@class = 'score-panel']")
                    citations = stats.xpath(".//div/dl[@class = 'scholarly-citation-counts']/dd/a[contains(text(), 'Dimensions')]/strong[1]/text()").get(),
                    readership = stats.xpath(".//div/h2[contains(text(), 'Readers on')]/following-sibling::dl/dd/a/strong[1]/text()").get(),
                    tweets = stats.xpath(".//div/h2[contains(text(), 'Mentioned by')]/following-sibling::dl/dd/a[contains(text(), ' tweeter')]/strong[1]/text()").get(),
                    news_mentions = stats.xpath(".//div/h2[contains(text(), 'Mentioned by')]/following-sibling::dl/dd/a[contains(text(), ' news outlets')]/strong[1]/text()").get()
                


                pub_loc = paper.xpath(".//*[contains(text(), 'Published In')]/following-sibling::ul/li/a/text()").get()
                if(pub_loc is None):
                    pub_loc = paper.xpath("//*[contains(text(), 'Published In')]/following-sibling::ul/li/text()").get()
                
                yield{
                    'title': paper.xpath(".//section[@id = 'individual-info']/header/h1/text()").get(),
                    'authors': paper.xpath(".//ul[@id = 'individual-DukeAuthors']/following-sibling::ul[1]/li/text()").getall(),
                    'published_date': paper.xpath(".//ul[@id = 'individual-PublishedDate']/li[1]/text()").get(),
                    'doi': paper.xpath(".//h3[contains(text(),'Digital Object Identifier (DOI)')]/following-sibling::ul[1]/li/text()").get(),
                    'abstract': paper.xpath(".//div[@class = 'abstract']/p/text()").get(),
                    'publication_location': pub_loc,
                    'link': paper.xpath(".//h3[contains(text(), 'Full Text')]/following-sibling::ul[1]/li[1]/a/@href").get(),

                    'citations': citations,
                    'readership': readership,
                    'tweets': tweets,
                    'news_mentions': news_mentions
                }
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.save_screenshot("articlepage.png")