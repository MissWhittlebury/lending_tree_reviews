import scrapy

from lt_reviewsbot.item_loaders import ReviewLoader


class LtReviewsSpider(scrapy.Spider):

    name = "lt_reviews"

    def __init__(self, *args, **kwargs):
        super(LtReviewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]

    # def start_requests(self):
    #     urls = [
    #         'https://www.lendingtree.com/reviews/mortgage/loansnap/39777117'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        reviews = response.xpath(
            '//section[@class="lenderReviews"]//div[contains(@class,"mainReviews")]')
        for review in reviews:
            yield ReviewLoader.load_review(review)

        next_link = response.xpath('//a[text()="Next"]/@href').get()
        if next_link:
            yield scrapy.Request(url=next_link, callback=self.parse_next)

        prev_link = response.xpath('//a[text()="Prev"]/@href').get()
        if prev_link:
            yield scrapy.Request(url=prev_link, callback=self.parse_prev)

    def parse_next(self, response):
        reviews = response.xpath(
            '//section[@class="lenderReviews"]//div[contains(@class,"mainReviews")]')
        for review in reviews:
            yield ReviewLoader.load_review(review)

        next_link = response.xpath('//a[text()="Next"]/@href').get()
        if next_link:
            yield scrapy.Request(url=next_link, callback=self.parse_next)

    def parse_prev(self, response):
        reviews = response.xpath(
            '//section[@class="lenderReviews"]//div[contains(@class,"mainReviews")]')
        for review in reviews:
            yield ReviewLoader.load_review(review)

        prev_link = response.xpath('//a[text()="Prev"]/@href').get()
        if prev_link:
            yield scrapy.Request(url=prev_link, callback=self.parse_prev)
