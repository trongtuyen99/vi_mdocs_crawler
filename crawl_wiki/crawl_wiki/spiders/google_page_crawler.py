import scrapy
from bs4 import BeautifulSoup

class GooglePageSpider(scrapy.Spider):
    name = "google_content"

    def start_requests(self):
        with open('google_links.txt', 'r') as file:
            urls = file.readlines()
        # urls = [
        #     'https://vietnambiz.vn/bo-may-quan-lieu-bureaucracy-la-gi-dac-diem-va-han-che-20190923100510896.htm',
        # ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url = response.url
        all_content = []
        try:
            html_parse = BeautifulSoup(response.body, 'html.parser')
            
            for para in html_parse.find_all(['p', 'li']):
                try:
                    all_content.append(para.get_text())
                except:
                    pass
        except Exception as e:
            print(f"Get content wiki {url} exception: {e}")
        
        yield {url: '\n'.join(all_content)}