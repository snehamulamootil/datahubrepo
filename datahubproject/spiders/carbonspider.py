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

        next_page = response.css('a.Pagination__NavItem.Link.Link--primary::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f'Paginating to: {next_page_url}')
            yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_product(self, response):
        item = DatahubprojectItem()
       # item['breadcrumbs'] =
        item['primary_image_url'] = response.css('img.Image--fadeIn::attr(src)').get()
        item['brand'] = response.css('h2.ProductMeta__Vendor.Heading.u-h1 a::text').get()
        item['product_name'] = response.css('h1.ProductMeta__Title.Heading::text').get()
        item['price'] = response.css('span.ProductMeta__Price.Price::text').get()
        item['reviews'] = len(response.css('div.yotpo-review'))
        item['colour'] = response.css('input.ColorSwatch__Radio::attr(value)').get()
        item['sizes'] = response.css('div.ProductForm__Option.ProductForm__Option--labelled label::text').getall()
        item['description'] = response.css('div.Faq__Answer.Rte p span::text').get()
        item['product_url'] = response.url
        item['image_urls'] = response.css('img.Image--fadeIn::attr(src)').getall()

        json_data = response.css('script[type="application/json"][data-product-data]::text').get()
        if json_data:
            try:
                data = json.loads(json_data)
                item['product_id'] = data.get('id')
                # Safely get the SKU from the first variant if available
                variants = data.get('variants', {}).get('nodes', [])
                if variants:
                    item['sku'] = variants[0].get('sku')
                else:
                    item['sku'] = None
            except Exception:
                item['sku'] = None
                item['product_id'] = None
        else:
            item['sku'] = None
            item['product_id'] = None

        yield item

