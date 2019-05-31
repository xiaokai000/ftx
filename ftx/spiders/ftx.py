import datetime
import re
import time
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from ftx.conn import Mongodb, RedisClient

class FtxSpider(RedisSpider):
    name = 'ftx'
    # 注意redis-key的格式：

    # 可选：等效于allowd_domains()，__init__方法按规定格式写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        self.col = Mongodb().db['old_ftx']
        # 修改这里的类名为当前类名
        super(FtxSpider, self).__init__(*args, **kwargs)


    def start_requests(self):
        for i in self.col.find({}):
            yield  Request(

                url= i['newhouse_url'],
                meta = {
                    'url' : i['newhouse_url'],
                    '_id' : i['_id'],
                    'province': i['province'],
                    'city': i['city'],
                    'newhouse_url': i['newhouse_url']
                }
            )

    def parse(self, response):
        all_pages = response.xpath('//*[@id="sjina_C01_47"]/ul/li[2]/a[last()]/@href').extract()
        all_urls = [response.meta['url']]
        if all_pages:
            all_page_number = all_pages[0].split('b9')[-1].replace('/', '')

            for i in range(1, int(all_page_number)):
                all_urls.append(response.meta['url'] + 'b9' + str(i))


        for detail_url in all_urls:
            yield Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={
                    '_id': response.meta['_id'],
                    'province': response.meta['province'],
                    'city': response.meta['city'],
                    'newhouse_url': response.meta['newhouse_url']
                }

            )

    def parse_detail(self, response):
        for li in response.xpath('//*[@id="newhouse_loupai_list"]/ul/li'):
            a = li.xpath('.//div[@class="nhouse_price"]/span/text()').extract()
            unit = li.xpath('.//div[@class="nhouse_price"]/em/text()').extract()
            areas = li.xpath('//*[@id="sjina_C23_04"]/text()').extract()

            if a:
                try:
                    price = int(a[0])
                except:
                    return
                if '万元/套' in unit[0] and areas:
                    flag = False
                    for area in areas:
                        try:
                            area = area.strip()
                            low_area = re.search('(.*)(\d+)(.*)', area).group(1).strip().split('~')[0]
                            if low_area:
                                price = int((price * 10000) / int(low_area))
                                flag = True
                                break
                        except:
                            continue
                    if not flag:
                        continue

                new_id = response.meta['_id'].split('@')[0] + '@' + str(datetime.date.today())
                self.col.update({'_id': new_id},{'$set':
                                                     {'date': str(datetime.date.today()),
                                                      'province': response.meta['province'],
                                                      'city': response.meta['city'],
                                                      'newhouse_url': response.meta['newhouse_url']
                                                      },
                                                 '$push':{'new_house_price_list': price}},
                                                    upsert=True)
