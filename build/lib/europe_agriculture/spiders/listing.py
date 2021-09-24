# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser

from europe_agriculture.items import listingUrlFieldItem


class ListingSpider(scrapy.Spider):
    name = 'listing'
    allowed_domains = ['europe-agriculture.com']
    start_urls = ['https://www.europe-agriculture.com/used-farming-equipments/f7/farming-equipments-ads.html']

    def parse(self, response):
        categoryurl = response.xpath('//div[@class="categories"]/div[@class="row"]/a/@href').extract()
        catname = response.xpath('//div[@class="categories"]/div[@class="row"]/a/@title').extract()
        for name, url in zip(catname, categoryurl):
            url = 'https://www.europe-agriculture.com' + url
            yield scrapy.Request(url=url, callback=self.parseCategory, meta={'cat1_name': name, 'buying_format': 'sale'})
            # break
        rentalurl = 'https://www.europe-agriculture.com/rental-farming-equipments/fl7/farming-equipments-ads.html'
        yield scrapy.Request(url=rentalurl, callback=self.parserental)

    # rental url
    def parserental(self, response):
        categoryurl = response.xpath('//*[@id="categories-1"]/li/a/@href').extract()
        catname = response.xpath('//*[@id="categories-1"]/li/a/@title').extract()
        for name, caturl in zip(catname, categoryurl):
            caturl = 'https://www.europe-agriculture.com' + caturl
            if 'https://www.planet-trucks.com' not in caturl:
                yield scrapy.Request(url=caturl, callback=self.parseCategory, dont_filter=True,meta={'cat1_name': name, 'buying_format': 'rent'})

    def parseCategory(self, response):
        # open_in_browser(response)
        category_url = response.xpath('//*[@id="variants"]/li/a/@href').extract()
        category_name = response.xpath('//*[@id="variants"]/li/a/@title').extract()
        # single level categories to call parseListingMethod
        if len(category_url) == 0:
            yield scrapy.Request(url=response.url, callback=self.parseListing,
                                 meta={'cat1_name': response.meta['cat1_name'],
                                       'cat2_name': response.meta['cat1_name'],
                                       'cat3_name': response.meta['cat1_name'],
                                       'buying_format': response.meta['buying_format']},
                                 dont_filter=True)

        else:
            for link, name in zip(category_url, category_name):
                categoryUrl = 'https://www.europe-agriculture.com' + str(link)
                cat2_name = name.replace('used', '').replace('Rental', '').strip()
                yield scrapy.Request(url=categoryUrl, callback=self.parsesubCategory,
                                     meta={'cat1_name': response.meta['cat1_name'],
                                           'cat2_name': cat2_name,
                                           'buying_format': response.meta['buying_format']})

    def parsesubCategory(self, response):
        sub_category_url = response.xpath('//*[@id="sub-variants"]/li/a/@href').extract()
        sub_category_name = response.xpath('//*[@id="sub-variants"]/li/a/@title').extract()

        # single level categories to call parseListingMethod
        if len(sub_category_url) == 0:
            yield scrapy.Request(url=response.url, callback=self.parseListing,
                                 meta={'cat1_name': response.meta['cat1_name'],
                                       'cat2_name': response.meta['cat2_name'],
                                       'cat3_name': response.meta['cat2_name'],
                                       'buying_format': response.meta['buying_format']},
                                 dont_filter=True)

        else:
            for link, name in zip(sub_category_url, sub_category_name):
                subcategoryUrl = 'https://www.europe-agriculture.com' + str(link)
                cat3_name = name.replace('used', '').replace('Rental', '').strip()
                yield scrapy.Request(url=subcategoryUrl, callback=self.parseListing,
                                     meta={'cat1_name': response.meta['cat1_name'],
                                           'cat2_name': response.meta['cat2_name'],
                                           'cat3_name': cat3_name,
                                           'buying_format': response.meta['buying_format']})

    def parseListing(self, response):
        item = listingUrlFieldItem()
        data = response.xpath('//div[@id="vehicles"]/div/div[contains(@class," page-break-inside ")]')
        for selector in data:
            final_ul = selector.xpath('./a/@href').extract_first("")
            if final_ul:
                item_url = 'https://www.europe-agriculture.com' + selector.xpath('./a/@href').extract_first("")
            else:
                item_url = 'https://www.europe-agriculture.com' + selector.xpath('./div/@data-ihref').extract_first("")

            thum_url = selector.xpath('.//*[@class="corner img-responsive lazy-load"]/@data-src').extract_first('')
            if thum_url is not None:
                if 'no_photo.png' in thum_url:
                    thum_url = ''
            else:
                thum_url = ''

            title = selector.xpath('.//*[@class="title"]/h2/text()').extract_first("").strip()
            price = selector.xpath('.//*[@class="row infos listing-price"]/span/text()').extract_first("")
            if response.meta['buying_format'] == 'rent':
                if '-' in price:
                    price = price.split('-')[0]
                else:
                    price = price
                currency = 'EUR'
            else:
                if price is not None:
                    currency = 'EUR'
                else:
                    price = ''
                    currency = ''

            country = selector.xpath('.//*[@class="font-weight-normal listing-geo inline-block width-pct-100"]//small[1]/text()').extract_first()
            if country is not None:
                country = country.replace(' - ', '')

            city = selector.xpath('.//*[@class="font-weight-normal listing-geo inline-block width-pct-100"]//small[2]/text()').get("")
            if ' - ' in city:
                city = ''

            city = city.strip()

            item['item_url'] = item_url
            item['thumbnail_url'] = thum_url
            item['title'] = title
            item['item_custom_info'] = {
                'buying_format': response.meta['buying_format'],
                'price': price or '',
                'currency': currency or '',
                'country': country or '',
                'city': city
            }
            item['category'] = {
                'cat1_name': response.meta['cat1_name'],
                'cat2_name': response.meta['cat2_name'],
                'cat3_name': response.meta['cat3_name']
            }
            yield item

        next_page_url = response.xpath("//*[contains(text(),'Next page')]/@data-href").extract_first()
        # if next_page_url is None:
        #     try:
        #         next_page_url = response.xpath('//*[@id="vehicles"]/div[3]/div[1]/div/div[1]/a[last()]/@data-href').extract_first()
        #     except:
        #         next_page_url = ''

        if next_page_url is not None:

            url = 'https://www.europe-agriculture.com' + next_page_url
            self.logger.debug("Next Page Url %s", next_page_url)
            yield scrapy.Request(url=url, callback=self.parseListing, meta={'cat1_name': response.meta['cat1_name'],
                                                                            'cat2_name': response.meta['cat2_name'],
                                                                            'cat3_name': response.meta['cat3_name'],
                                                                            'buying_format': response.meta['buying_format']})

#
#
# from scrapy.cmdline import execute
# execute("scrapy crawl listing".split())