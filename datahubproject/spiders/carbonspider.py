import scrapy
import json
from datahubproject.items import DatahubprojectItem


class CarbonspiderSpider(scrapy.Spider):
    name = "carbonspider"
    allowed_domains = ["carbon38.com"]
    start_urls = ["https://www.carbon38.com/shop-all-activewear/tops"]

    def parse(self, response):
         # Crawl all products on the current page
        product_links = response.css('div.ProductItem__Info h2.ProductItem__Title a::attr(href)').getall()
        for link in product_links:
            full_link = response.urljoin(link)
            yield scrapy.Request(full_link, callback=self.parse_product)


    def parse_product(self, response):
        item = DatahubprojectItem()
       # item['breadcrumbs'] =
        item['primary_image_url'] = response.css('img.fotorama__img::attr(src)').get()
        item['brand'] = response.css('h2.ProductMeta__Vendor.Heading.u-h1::text').get()
        item['product_name'] = response.css('h1.ProductMeta__Title.Heading::text').get()
        item['price'] = response.css('span.ProductMeta__Price.Price::text').get()
        item['reviews'] = len(response.css('div.yotpo-review'))
        item['colour'] = response.css('input.ColorSwatch__Radio::attr(value)').get()
       # item['sizes'] =
       # item['description'] =
       # item['sku'] =
       # item['product_id'] =
       # item['product_url'] =
       # item['image_urls'] =
        yield item
