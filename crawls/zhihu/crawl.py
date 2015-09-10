from zhihu.spiders.explore_spider import ExplorSpider

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.conf import settings


print settings['MONGO_URI']



process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'MONGO_URI' : "localhost:27017",
    'MONGO_DATABASE' : "circle",
    'MONGO_COLLECTION' : "zhihu_explore",
    'ITEM_PIPELINES': {
        'zhihu.pipelines.JsonWriterPipeline': 100,
        'zhihu.pipelines.MongoDBPipeline': 800
    }
})

process.crawl(ExplorSpider)
process.start() # the script will block here until the crawling is finished