from http import HTTPStatus
import json
import os
import subprocess

from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerProcess

from lt_reviewsbot.spiders.spider import LtReviewsSpider


app = Flask(__name__)

@app.route('/reviews/<lender_name>')
def reviews(lender_name):
    url = request.args.get('url')
    if url is None:
        return jsonify({'message': 'url parameter is required'}), \
               HTTPStatus.BAD_REQUEST.value
    if 'lendingtree.com' not in url:
        return jsonify({'message': 'only lendingtree.com reviews are supported'}), \
               HTTPStatus.BAD_REQUEST.value
    pathname = os.path.join('json_results', f'{lender_name}.json')
    if os.path.exists(pathname):
        os.remove(pathname)
    subprocess.check_output(['scrapy', 'crawl', 'lt_reviews', '-a',
                            f'start_url={url}', '-o', pathname, '-t', 'json'])

    with open(pathname, 'r') as j:
        json_str = j.read()

    if not json_str:
        return json.dumps([]), HTTPStatus.OK.value

    return jsonify(json.loads(json_str)), HTTPStatus.OK.value


if __name__ == '__main__':
    url = 'https://www.lendingtree.com/reviews/personal/cashnetusa/81638970'
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'items.json'
    })
    process.crawl(LtReviewsSpider, start_url=url)
    process.start()

