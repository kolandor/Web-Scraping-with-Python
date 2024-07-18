import scrapy


class SpidQouSpider(scrapy.Spider):
    name = "spid_qou"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        
        for qoute in quotes:
            qoute_text = qoute.xpath('.//span[@class="text"]/text()').get()
            qoute_author = qoute.xpath('.//small[@class="author"]/text()').get()
            
            yield {
                    "quoute" : qoute_text,
                    "author" : qoute_author
                }
