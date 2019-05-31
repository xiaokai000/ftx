import requests
import re
import lxml.html
import random
etree = lxml.html.etree
import datetime
from ftx.conn import Mongodb, RedisClient

col = Mongodb().db['old_ftx']

p = ['https://101.66.53.59:4267', 'https://100.68.32.163:2444', 'https://180.112.39.51:4263', 'https://114.239.254.254:4236', 'https://117.92.131.156:2444']


for item in col.find({}):
    response = requests.get(item['newhouse_url']).text
    response = etree.HTML(response)
    all_pages = response.xpath('//*[@id="sjina_C01_47"]/ul/li[2]/a[last()]/@href')

    all_urls = [item['newhouse_url']]
    if all_pages:
        all_page_number = all_pages[0].split('b9')[-1].replace('/', '')

        for i in range(1, int(all_page_number)+1):
            all_urls.append(item['newhouse_url'] + 'b9' + str(i))

    for detail_url in all_urls:
        response = requests.get(detail_url).text
        print(response)
        response = etree.HTML(response)

        for li in response.xpath('//*[@id="newhouse_loupai_list"]/ul/li'):
            a = li.xpath('.//div[@class="nhouse_price"]/span/text()')
            unit = li.xpath('.//div[@class="nhouse_price"]/em/text()')
            areas = li.xpath('//*[@id="sjina_C23_04"]/text()')
            print(unit)
            if a:
                try:
                    price = int(a[0])
                except:
                    continue

                if '万元/套'.encode('gb2312') in unit[0] and areas:

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

                # new_id = item['_id'].split('@')[0] + '@' + str(datetime.date.today())
                # col.update({'_id': new_id},{'$set':
                #                                      {'date': str(datetime.date.today()),
                #                                       'province': item['province'],
                #                                       'city': item['city'],
                #                                       'newhouse_url': item['newhouse_url']
                #                                       },
                #                                  '$push':{'new_house_price_list': price}},
                #                                     upsert=True)