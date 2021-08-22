import scrapy
from bs4 import BeautifulSoup
import urllib
from scrapy.linkextractors import LinkExtractor
custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
google_domains = ('https://www.google.', 
                'https://google.', 
                'https://webcache.googleusercontent.', 
                'http://webcache.googleusercontent.', 
                'https://policies.google.',
                'https://support.google.',
                'https://maps.google.',
                'https://accounts.google.com',
                'http://go.microsoft.',
                'https://go.microsoft.',
                'http://www.microsofttranslator.com',
                'https://www.youtube.com',
                'https://www.facebook.com',
                'http://help.bing.',
                'http://creativecommons.org')
except_extends = ('.pdf', '.docx', '.ppt')

class GoogleLinkSpider(scrapy.Spider):
    name = "google_link"

    def start_requests(self):

        with open('google_queries.txt', 'r') as file:
            urls = file.readlines()
        for url in urls:
            url = url.replace('.google.', '.bing.')
            yield scrapy.Request(url=url, callback=self.parse,\
             headers={"User-Agent": custom_user_agent})

    def parse(self, response):
        url = response.url
        all_links = set()
        crawled_source = set()
        try:
            html_parse = BeautifulSoup(response.body, 'html.parser')
            
            for para in html_parse.findAll('a', href=True):
                try:
                    link = para.get('href')
                    if link.startswith('http') and not link.startswith(google_domains) and\
                    'wikipedia' not in link and not link.endswith(except_extends):
                        all_links.add(link)
                    # if link.startswith('/url?q=https'):
                    #     source = link.split('/')[3]
                    #     if source not in crawled_source:
                    #         crawled_source.add(source)
                    #         use_link = link[7:].split('&')[0]
                    #         if not use_link.startswith(google_domains) and 'wikipedia' not in use_link:
                    #             all_links.append(use_link)
                except:
                    pass

        except Exception as e:
            print(f"Get content wiki {url} exception: {e}")
        
        yield {url: list(all_links)}
