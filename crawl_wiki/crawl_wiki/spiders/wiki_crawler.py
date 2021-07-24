import scrapy
from bs4 import BeautifulSoup

class WikiContentSpider(scrapy.Spider):
    name = "wiki_content"

    def start_requests(self):
        with open('wiki_links.txt', 'r') as file:
            urls = file.readlines()
        # urls = [
        #     'https://vi.wikipedia.org/wiki/B%E1%BB%99_m%C3%A1y_quan_li%C3%AAu',
        # ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url = response.url
        all_content = []
        try:
            html_parse = BeautifulSoup(response.body, 'html.parser')
            
            for para in html_parse.find("div", id="bodyContent"):
                try:
                    all_content.append(para.get_text())
                except:
                    pass
        except Exception as e:
            print(f"Get content wiki {url} exception: {e}")
        
        yield {url: '\n'.join(all_content)}