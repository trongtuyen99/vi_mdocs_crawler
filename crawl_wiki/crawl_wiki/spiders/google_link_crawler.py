import scrapy
from bs4 import BeautifulSoup
import urllib
from scrapy.linkextractors import LinkExtractor
google_domains = ('https://www.google.', 
                'https://google.', 
                'https://webcache.googleusercontent.', 
                'http://webcache.googleusercontent.', 
                'https://policies.google.',
                'https://support.google.',
                'https://maps.google.',
                'https://accounts.google.com')
class GoogleLinkSpider(scrapy.Spider):
    name = "google_link"

    def start_requests(self):

        with open('google_queries.txt', 'r') as file:
            urls = file.readlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url = response.url
        all_links = []
        crawled_source = set()
        try:
            html_parse = BeautifulSoup(response.body, 'html.parser')
            
            for para in html_parse.findAll('a', href=True):
                link = para.get('href')
                if link.startswith('/url?q=https'):
                    source = link.split('/')[3]
                    if source not in crawled_source:
                        crawled_source.add(source)
                        use_link = link[7:].split('&')[0]
                        if not use_link.startswith(google_domains) and 'wikipedia' not in use_link:
                            all_links.append(use_link)

        except Exception as e:
            print(f"Get content wiki {url} exception: {e}")
        
        yield {url: all_links}
