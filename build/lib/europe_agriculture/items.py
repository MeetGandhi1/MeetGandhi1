# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EuropeAgricultureItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_main_category = scrapy.Field()
    item_main_category_id = scrapy.Field()
    item_category = scrapy.Field()
    item_source_category_id = scrapy.Field()
    item_sub_category = scrapy.Field()
    item_source_sub_category_id = scrapy.Field()
    # Company = scrapy.Field()
    item_title = scrapy.Field()
    year = scrapy.Field()
    serial_number = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    vendor_name = scrapy.Field()
    vendor_country = scrapy.Field()
    vendor_state = scrapy.Field()
    vendor_city = scrapy.Field()
    vendor_url = scrapy.Field()
    img_url = scrapy.Field()
    thumbnail_url = scrapy.Field()
    item_url = scrapy.Field()
    details = scrapy.Field()
    extra_fields = scrapy.Field()
    source_item_id = scrapy.Field()
    buying_format = scrapy.Field()
    price_original = scrapy.Field()
    vendor_contact_url = scrapy.Field()
    vendor_email = scrapy.Field()
    vendor_email1 = scrapy.Field()
    vendor_email2 = scrapy.Field()
    vendor_email3 = scrapy.Field()
    vendor_location = scrapy.Field()
    vendor_address = scrapy.Field()
    vendor_address2 = scrapy.Field()
    vendor_zipcode = scrapy.Field()
    vendor_phone = scrapy.Field()
    vendor_phone2 = scrapy.Field()
    vendor_logo_url = scrapy.Field()
    vendor_contact = scrapy.Field()
    vendor_contact_designation = scrapy.Field()
    vendor_contact2 = scrapy.Field()
    vendor_contact2_designation = scrapy.Field()
    vendor_fax = scrapy.Field()
    vendor_website = scrapy.Field()
    vendor_facebook = scrapy.Field()
    vendor_twitter = scrapy.Field()
    vendor_linkedin = scrapy.Field()
    vendor_skype = scrapy.Field()
    vendor_services = scrapy.Field()
    vendor_categories = scrapy.Field()
    vendor_manufacturers = scrapy.Field()
    vendor_comments = scrapy.Field()

    city = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    thumbnail_s3_path = scrapy.Field()
    auction_ending = scrapy.Field()
    pass


class listingUrlFieldItem(scrapy.Item):
    item_custom_info = scrapy.Field()
    category = scrapy.Field()
    item_url = scrapy.Field()
    thumbnail_url = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    pass


class categoryFieldItem(scrapy.Item):
    MasterLevel1 = scrapy.Field()
    MasterLevel1Id = scrapy.Field()
    MasterLevel2 = scrapy.Field()
    MasterLevel2Id = scrapy.Field()

    pass





