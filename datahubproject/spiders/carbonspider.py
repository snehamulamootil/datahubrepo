import scrapy
from datahubproject.items import DatahubprojectItem


class CarbonspiderSpider(scrapy.Spider):
    name = "carbonspider"
    allowed_domains = ["carbon38.com"]
    start_urls = ["https://www.carbon38.com/product/tessa-top-primary-stripe"]

    def parse(self, response):
         # Crawl all products on the current page
        products = response.css('div.ProductItem').getall()
        for product in products:
            yield response.follow(product, callback=self.parse_product)

        # Go to next page (pagination)
        next_page = response.css('a.action.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item = DatahubprojectItem()
        item['breadcrumbs'] =
        item['primary_image_url'] = response.css('img.ProductItem__Image::attr(src)').get()
        item['brand'] = response.css('h3.ProductItem__Designer::text').get()
        item['product_name'] = response.css('h2.ProductItem__Title.Heading a::text').get()
        item['price'] = response.css('span.ProductItem__Price.Price::text').get()
        item['reviews'] = len(response.css('div.yotpo-main-layout.yotpo-main-reviews-widget .yotpo-review'))
        item['colour'] = response.css('input.ColorSwatch__Radio::attr(value)').get()
        item['sizes'] =
        item['description'] =
        item['sku'] =
        item['product_id'] =
        item['product_url'] =
        item['image_urls'] =
        yield item
        pass

