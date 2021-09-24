 # -*- coding: utf-8 -*-
import scrapy
import logging
import requests
from europe_agriculture.items import EuropeAgricultureItem
from scrapinghub import ScrapinghubClient
import re
class DetailSpider(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['europe-agriculture.com']
    start_urls = ['https://www.europe-agriculture.com']
    project_id = 447697
    # custom_settings = {
    #     'CLOSESPIDER_TIMEOUT': 3600
    # }

    def __init__(self, collection_name=None, *args, **kwargs):
        super(DetailSpider, self).__init__(*args, **kwargs)
        global current_collection, url, listing_urls,thumb_urls,category_names, collection_keys, foo_store,title, country, price, currency,city, buying_format, subcategory_names, maincategory
        listing_urls = []
        maincategory = []
        category_names  = []
        collection_keys = []
        thumb_urls = []
        title = []
        country = []
        city = []
        price = []
        subcategory_names = []
        buying_format = []
        currency = []
        current_collection = ''

        logging.basicConfig()
        logger = logging.getLogger('logger')
        apikey = 'a77f8d9112a14cd6bfc4e3734261b2aa'
        client = ScrapinghubClient(apikey)
        project = client.get_project(self.project_id)
        collections = project.collections
        if not collection_name:
            collection_list = collections.list()[-1]
            collection_name = collection_list.get('name')
            foo_store = collections.get_store(collection_name)
            print("MyStore", collection_name)
        else:
            foo_store = collections.get_store(collection_name)
        current_collection = str(collection_name)
        print("Getting Items from collection" + str(collection_name))
        print("Length of collection" + str(foo_store.count()))

        for elem in foo_store.iter():
            collection_keys.append(elem['_key'])
            maincategory.append(str(elem['category'].get('cat1_name')))
            category_names.append(str(elem['category'].get('cat2_name')))
            subcategory_names.append(str(elem['category'].get('cat3_name')))
            listing_urls.append(elem['item_url'])
            thumb_urls.append(str(elem['thumbnail_url']))
            title.append(str(elem['title']))
            country.append(str(elem['item_custom_info'].get('country')))
            city.append(str(elem['item_custom_info'].get('city')))
            price.append(str(elem['item_custom_info'].get('price')))
            currency.append(str(elem['item_custom_info'].get('currency')))
            buying_format.append(str(elem['item_custom_info'].get('buying_format')))
        print("Fetched from collection" + str(collection_name))

    def parse(self, response):
        k = 0
        for listing_url in listing_urls:
            collection_item_key = collection_keys[k]
            thum_url = thumb_urls[k]
            maincat = maincategory[k]
            catname = category_names[k]
            subcatname = subcategory_names[k]
            title_ = title[k]
            country_ = country[k]
            city_ = city[k]
            currency_ = currency[k]
            price_ = price[k]
            buy_format = buying_format[k]
            k = k + 1
            source_item_id = 'ironlist' + str(self.project_id) + collection_item_key
            yield scrapy.Request(url=listing_url, callback=self.parseDetail,
                                 meta={'source_item_id': source_item_id, 'collection_item_key': collection_item_key,'catname':catname,'subcatname':subcatname,
                                       'listing_url': listing_url,'thum_url':thum_url, 'title':title_,'buying_format': buy_format,'maincat':maincat,
                                       'price': price_, 'currency':currency_,'country': country_, 'city':city_})

    def parseDetail(self, response):

        item = EuropeAgricultureItem()

        item_title = response.meta['title']
        item['item_title'] =item_title

        details = response.xpath('//*[@id="features-content"]/div/text()').getall()
        joine_string=''
        if joine_string=='':
            for i in details:
                i=i.strip()
                joine_string = joine_string + str(i)
            print(joine_string)
            item['details'] = str(item_title)+'-->'+joine_string[0:300]

        data = {}
        for row in response.xpath('//*[@class="col-sm-4 print-sm-12"][1]/div/table[1]/tbody/tr'):
            key = row.xpath('td[1]//text()').extract_first()
            value = row.xpath('td[2]//text()').extract_first()
            data[key] = value


        vendor_name = response.xpath('//*[@class="margin-top-15"]/h2/text()').extract_first()
        if vendor_name is not None:
            vendor_name =vendor_name.strip()
        vendor_phone = response.xpath('//*[@class="text-normal visible-print hide margin-auto margin-bottom-20"]/text()').extract()
        if len(vendor_phone) == 2:
            vendor_phone = vendor_phone[-1].strip()
        else:
            vendor_phone = ''

        vendor_address = response.xpath('//*[@class="margin-bottom-10 map-address"]/span/text()|//*[@class="margin-bottom-10 map-address"]/strong/span/text()').extract()
        address = []

        if len(vendor_address) != 0 :
            location = vendor_address[-1]
            for i in vendor_address :
                address.append(i)
            address = ','.join(address)
        else:
            address = ''
            location = ''


        data1 = {}
        for row in response.xpath('//*[@class="col-sm-4 print-sm-12"][2]/div/table[1]/tbody/tr'):
            key = row.xpath('td[1]//text()').extract_first()
            value = row.xpath('td[2]//text()').extract_first()
            data1[key] = value

        make = data.get('Make')
        if make is not None:
            if '--' in make:
                make = ''
        else:
            make = ''
        model = data.get('Model')
        if model is not None:
            if '--' in model:
                model = ''
        else:
            model = ''

        year = data.get('Year')
        if year is not None:
            if '-' not in year:
                year = int(year.split('/')[-1])
            else:
                year = ''
        else:
            year = ''

        power = data1.get('Power')
        if power is not None:
            if '-' in power:
                power = ''
            else:
                power = power.replace('HP','')
        else:
            power = ''

        hours = data1.get('Number of hours')
        if hours is not None:
            if '-' in hours:
                hours = ''
            else:
                hours = hours.replace('hours', '')
        else:
            hours = ''

        miles = data1.get('Mileage')
        if miles is not None:
            if '-' in miles:
                miles = ''
            else:
                miles = miles.replace('km', '')
        else:
            miles = ''

        item['buying_format'] = response.meta['buying_format']
        item['extra_fields'] = {'Mileage': miles,
                                'Power': power,
                                'hours': hours}

        item['city'] = response.meta['city']
        item['country'] = response.meta['country']
        item['img_url'] = response.xpath('//*[@rel="diaporama"]/@href').extract()[:5]
        item['item_main_category'] = response.meta['maincat']
        item['item_main_category_id'] = response.meta['maincat']
        item['item_category'] = response.meta['catname']
        item['item_source_category_id'] = response.meta['catname']
        item['item_source_sub_category_id'] = response.meta['subcatname']
        item['item_sub_category'] = response.meta['subcatname']
        item['item_url'] = response.meta['listing_url']
        item['make'] = make
        item['model'] = model

        try:
            year = year or ''
            valid_year = 1900 <= int(re.findall(r'\d{4}', str(year))[0]) <= 2020
            if valid_year is True:
                year = re.findall(r'\d{4}', str(year))[0]
                item['year'] = year
        except Exception as e:
            # print('Invalid year in: ', respnse.url)
            item['year'] = ""

        item['thumbnail_url'] = str(response.meta['thum_url']).replace('_th.jpg','.jpg')
        if 'http' not in item['thumbnail_url']:
            item['thumbnail_url'] = ''
            item['thumbnail_s3_path'] = '/thumbnailimagenotfound.jpg'
        else:
            item['thumbnail_s3_path'] = ''



        price = response.meta['price']
        try:
            price_data = re.sub('[^0-9,.]', "", price)
            item['price'] = int(eval(price_data.replace(",", "")))
            if item['price']:
                item['price_original'] = item['price']
                item['currency'] = response.meta['currency'] or ''
        except:
            item['price'] = item['currency'] = ''

        item['currency'] = response.meta['currency'] or ''
        item['vendor_country'] = location or ''
        item['vendor_location'] = location or ''
        item['vendor_name'] = vendor_name or ''
        if not item['vendor_name']:
            item['vendor_name'] = 'europe agriculture'
        item['vendor_phone'] = vendor_phone
        item['vendor_address'] = address

        collection_item_key = response.meta['collection_item_key']
        item['source_item_id'] = response.meta['source_item_id']
        foo_store.delete(collection_item_key)
        yield item

    def closed(self, resason):
        print("+++++++++++++++++++++++++++++")
        print("Close Spider Method")
        if resason == 'closespider_timeout':
            myurl = "https://app.scrapinghub.com/api/run.json?apikey=a77f8d9112a14cd6bfc4e3734261b2aa"
            formdata = {'project': self.project_id, 'spider': 'detail', 'collection_name': '' + current_collection}
            yield requests.post(myurl, formdata)
