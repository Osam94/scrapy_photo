import scrapy
from ..items import UnsplashImageItem
  # Убедитесь, что путь к вашему Item правильный

class UnsplashSpider(scrapy.Spider):
    name = 'photo_img'
    allowed_domains = ['unsplash.com']
    start_urls = ['https://unsplash.com/']
    def parse(self, response):
        # Извлекаем ссылки на категории 
        category_links = response.xpath('//a[contains(@href, "/t/")]/@href').extract()
        for link in category_links:
            yield response.follow(link, self.parse_category)

    def parse_category(self, response):
        # Извлекаем ссылки на изображения в категории 
        image_links = response.xpath('//a[contains(@href, "/photos/")]/@href').extract()
        for link in image_links:
            yield response.follow(link, self.parse_image)

        # Пагинация - извлечение следующей страницы категории, если она есть
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse_category)

    def parse_image(self, response):
        # Извлечение данных изображения
        item = UnsplashImageItem()
        item['image_url'] = response.xpath('//meta[@property="og:image"]/@content').extract_first()
        item['image_title'] = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        item['image_category'] = response.xpath('//a[contains(@href, "/t/")]/text()').extract_first()
        item['image_description'] = response.xpath('//meta[@property="og:description"]/@content').extract_first()
        item['image_author'] = response.xpath('//meta[@property="og:site_name"]/@content').extract_first()
        yield item
           