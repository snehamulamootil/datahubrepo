import scrapy


class CarbonspiderSpider(scrapy.Spider):
    name = "carbonspider"
    allowed_domains = ["carbon38.com"]
    start_urls = ["https://carbon38.com"]

    def parse(self, response):
        pass
