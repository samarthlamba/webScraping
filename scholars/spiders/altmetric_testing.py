# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium import webdriver
from shutil import which

class AltmetrictestingSpider(scrapy.Spider):
    name = 'altmetric_testing'
    allowed_domains = ['www.duke.altmetric.com'] 
    start_urls = [
        'https://duke.altmetric.com/details/2474443'
    ]

    def parse(self, response):
        attention_score = response.xpath("//strong[text() = 'Altmetric Attention Score']/following-sibling::strong[1]/text()").get()
        stats = response.xpath("//div[@class = 'score-panel']")
        citations = stats.xpath(".//div/dl[@class = 'scholarly-citation-counts']/dd/a[contains(text(), 'Dimensions')]/strong[1]/text()").get(),
        readership = stats.xpath(".//div/h2[contains(text(), 'Readers on')]/following-sibling::dl/dd/a/strong[1]/text()").get(),
        tweets = stats.xpath(".//div/h2[contains(text(), 'Mentioned by')]/following-sibling::dl/dd/a[contains(text(), ' tweeter')]/strong[1]/text()").get(),
        news_mentions = stats.xpath(".//div/h2[contains(text(), 'Mentioned by')]/following-sibling::dl/dd/a[contains(text(), ' news outlets')]/strong[1]/text()").get()

        ### Finding twitter stats
        twitter_stats = response.xpath("//h2[text() = 'Twitter Demographics']/following-sibling::div[@class = 'demographics-panel']/div[@class = 'demographics-group twitter']")
        
        # Twitter geographical breakdown
        twitter_geo = twitter_stats.xpath(".//div[@class = 'table-wrapper geo']/table//tr")
        
        # Pop the first element, corresponding to the title of the columns
        if twitter_geo:
            twitter_geo.pop(0)
        country_geo_twitter = []
        count_geo_twitter = []
        percentage_geo_twitter = []
        ## Append the information in each row to the appropriate arrays
        # Table denoting the geographic breakdown by country
        for row in twitter_geo:
            country_geo_twitter.append(row.xpath(".//td[1]/text()").get())
            count_geo_twitter.append(row.xpath(".//td[2]/text()").get())
            percentage_geo_twitter.append(row.xpath(".//td[3]/text()").get())
        
        # Twitter demographic breakdown
        twitter_demo = twitter_stats.xpath(".//div[@class = 'table-wrapper users']/table//tr")
        
        # Pop the first element, corresponding to the title of the columns
        # Declare empty arrays
        if twitter_demo:
            twitter_demo.pop(0)
        type_demo_twitter = []
        count_demo_twitter = []
        percentage_demo_twitter = []
 
        ## Append the information in each row to the appropriate arrays
        # Table denoting the demographic breakdown based on the type of audience
        for row in twitter_demo:
            type_demo_twitter.append(row.xpath(".//td[1]/text()").get())
            count_demo_twitter.append(row.xpath(".//td[2]/text()").get())
            percentage_demo_twitter.append(row.xpath(".//td[3]/text()").get())
        
        ### Finding mendeley stats
        mendeley_stats = response.xpath("//h2[text() = 'Mendeley readers']/following-sibling::div[@class = 'demographics-panel']")
        # Mendeley geographical breakdown
        mendeley_geo = mendeley_stats.xpath(".//div[@class = 'table-wrapper geo']/table//tr")
        
        # Pop the first element, corresponding to the title of the columns
        if mendeley_geo:
            mendeley_geo.pop(0)
        country_geo_mendeley = []
        count_geo_mendeley = []
        percentage_geo_mendeley = []

        ## Append the information in each row to the appropriate arrays
        # Table denoting the geographic breakdown by country
        for row in mendeley_geo:
            country_geo_mendeley.append(row.xpath(".//td[1]/text()").get())
            count_geo_mendeley.append(row.xpath(".//td[2]/text()").get())
            percentage_geo_mendeley.append(row.xpath(".//td[3]/text()").get())

        ## Mendeley demographic breakdown
        count_demo_mendeley = []
        percentage_demo_mendeley = []
        
        ## Append the information in each row to the appropriate arrays
        # Table denoting the demographic breakdown based on readers by professional status
        prof_status_demo_mendeley = []
        mendeley_demo_prof_status = mendeley_stats.xpath(".//div[@class = 'table-wrapper users']/table[1]//tr")
        # Pop the first element, corresponding to the title of the columns
        if mendeley_demo_prof_status:
            mendeley_demo_prof_status.pop(0)
        for row in mendeley_demo_prof_status:
            prof_status_demo_mendeley.append(row.xpath(".//td[1]/text()").get())
            count_demo_mendeley.append(row.xpath(".//td[2]/text()").get())
            percentage_demo_mendeley.append(row.xpath(".//td[3]/text()").get())

        ## Table denoting the demographic breakdown based on readers by discipline
        discipline_demo_mendeley = []
        mendeley_demo_discipline = mendeley_stats.xpath(".//div[@class = 'table-wrapper users']/table[2]//tr")
        
        # Pop the first element, corresponding to the title of the columns
        if mendeley_demo_discipline:
            mendeley_demo_discipline.pop(0)
        for row in mendeley_demo_discipline:
            discipline_demo_mendeley.append(row.xpath(".//td[1]/text()").get())
            count_demo_mendeley.append(row.xpath(".//td[2]/text()").get())
            percentage_demo_mendeley.append(row.xpath(".//td[3]/text()").get())
        
        # yield{
            # 'attention_score': attention_score,
            # 'citations': citations,
            # 'readership': readership,
            # 'tweets': tweets,
            # 'news_mentions': news_mentions
            # 'twitter_country': ,
            # 'twitter_count': country_geo_twitter[0],
            # 'twitter_percentage': percentage_geo_twitter[0]
        # }