# -*- coding: utf-8 -*-
__author__ = 'andrew'
import scrapy
import json

from zhihu.items import ZhihuItem


class ExplorSpider(scrapy.Spider):

    name = 'zhihu'
    allowed_domains = ["zhihu.com"]
    pageNum = 0

    #API
    EXPLORE_API = "http://www.zhihu.com/node/ExploreAnswerListV2?params="

    #页面个数
    PAGE_SIZE = 5

    #页数

    params = {"offset": pageNum * PAGE_SIZE, "type": "month"}
    pageNum += 1
    start_urls = [
         EXPLORE_API + json.dumps(params)
    ]



    def parse(self, response):
        PAGE_SIZE = self.PAGE_SIZE

        links = response.css(".explore-feed.feed-item .question_link")
        for link in links:
            href = link.xpath('@href').extract()[0]
            title = link.xpath('text()').extract()[0]
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = lambda response, title=title: self.parse_dir_contents(response, title))

        if len(links) < PAGE_SIZE:
            print "!!!!!done"
            return
        else:
            self.params["offset"] = self.pageNum * PAGE_SIZE
            request_url = self.EXPLORE_API + json.dumps(self.params)
            self.pageNum += 1
            yield scrapy.Request(request_url, self.parse)

    def parse_dir_contents(self, response, title):

        answers = response.css(".zh-question-answer-wrapper")
        for answer in answers:
            item = ZhihuItem()
            author = answer.css('.zm-item-answer-author-wrap a:nth-child(2)::text').extract()
            if author:
                author = author[0]
            else:
                author = '--'
            item['title'] = title
            item['agreeCount'] = answer.css('.count::text').extract()[0]
            item['author'] = author
            item['content'] = answer.css('.zm-item-rich-text').extract()[0]
            yield item

