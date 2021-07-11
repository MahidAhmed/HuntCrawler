import scrapy;
from ..items import HuntcrawlerItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    # page_number = 2
    start_urls = [
        'https://quotes.toscrape.com/login'
    ]
    def parse(self, response):
        token = response.css("form input::attr(value)").extract_first()
        return FormRequest.from_response(response, formdata={
            'cref_token': token,
            'username': 'mahid@gmail.com',
            'password': '1234'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        open_in_browser(response)
        items = HuntcrawlerItem()
        page_number = 2
        all_div_quotes = response.css("div.quote")
        for quotes in all_div_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tags = quotes.css('.tag::text').extract()
            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items

            next_page = 'https://quotes.toscrape.com/page/' + str(page_number) + '/'

            if page_number < 11:
                page_number += 1
                yield response.follow(next_page, callback=self.parsePagination)

    def parsePagination(self, response):
        items = HuntcrawlerItem()
        all_div_quotes = response.css("div.quote")
        for quotes in all_div_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tags = quotes.css('.tag::text').extract()
            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items
