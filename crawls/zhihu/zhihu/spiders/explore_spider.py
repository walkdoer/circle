__author__ = 'andrew'
import scrapy
import json

from zhihu.items import ZhihuItem

#  http://www.zhihu.com/node/ExploreAnswerListV2

class ExplorSpider(scrapy.Spider):
    name = 'zhihu_explore'
    allowed_domains = ["zhihu.com"]
    params = {"offset": 0, "type": "month"}
    start_urls = [
        "http://www.zhihu.com/node/ExploreAnswerListV2?params=" + json.dumps(params)
    ]

    def parse(self, response):
        for link in response.css(".explore-feed.feed-item .question_link"):
            href = link.xpath('@href').extract()[0]
            print(href)
            title = link.xpath('text()').extract()[0]
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = lambda response, title=title: self.parse_dir_contents(response, title))

    def parse_dir_contents(self, response, title):
        for answer in response.css(".zh-question-answer-wrapper"):
            item = ZhihuItem()
            item['title'] = title
            item['agreeCount'] = answer.css('.count::text').extract()[0]
            item['author'] = answer.css('.zm-item-answer-author-wrap a:nth-child(2)::text').extract()[0]
            item['content'] = answer.css('.zm-item-rich-text').extract()[0]
            yield item

