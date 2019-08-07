from datetime import datetime

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from lt_reviewsbot.items import Review


def strip_whitespace(self, iterator):
    if iterator:
        string = iterator[0]
        return string.strip()
    return ''

class ReviewLoader(ItemLoader):

    default_output_processor = TakeFirst()

    title_in = strip_whitespace
    content_in = strip_whitespace
    author_in = strip_whitespace

    def rating_in(self, iterator):
        style = iterator[0]
        rating = int(style.replace('width:', '').replace('%;',''))
        return int((rating / 100) * 5)

    def date_in(self, iterator):
        date = iterator[0].lower()
        date = date.replace('reviewed in', '').strip()
        return datetime.strptime(date, '%B %Y')

    def date_out(self, iterator):
        date = iterator[0]
        return date.strftime('%m/%Y')

    @staticmethod
    def load_review(review_selector):
        l = ReviewLoader(Review(), review_selector)
        l.add_xpath('title', 'div/p[@class="reviewTitle"]/text()')
        l.add_xpath('content', 'div/p[@class="reviewText"]/text()')
        l.add_xpath('author', 'div//p[@class="consumerName"]/text()')
        l.add_xpath('rating', 'div//div[@class="rating-stars-bar"]/@style')
        l.add_xpath('date', 'div//p[@class="consumerReviewDate"]/text()')
        return l.load_item()
