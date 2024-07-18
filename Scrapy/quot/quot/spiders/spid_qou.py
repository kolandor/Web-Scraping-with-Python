import scrapy


class SpidQouSpider(scrapy.Spider):
    name = "spid_qou"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    max_pages_follow_count = 2

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        
        for qoute in quotes:
            qoute_text = qoute.xpath('.//span[@class="text"]/text()').get()
            qoute_author = qoute.xpath('.//small[@class="author"]/text()').get()
            
            yield {
                    "quoute" : qoute_text,
                    "author" : qoute_author
                }
        self.max_pages_follow_count -= 1
        
        btn_next = response.xpath('//li[@class="next"]/a/@href').get()
        if btn_next and self.max_pages_follow_count:
            yield response.follow(btn_next, callback = self.parse)
