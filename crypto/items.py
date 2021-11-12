# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CryptoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    a_DT_date = scrapy.Field()
    a_DT_time = scrapy.Field()
    a_rank = scrapy.Field()
    b_name = scrapy.Field()
    c_symbol = scrapy.Field()
    d_price = scrapy.Field()
    e_P24h = scrapy.Field()
    f_P7d = scrapy.Field()
    g_marketCap = scrapy.Field()
    h_volumnUSD = scrapy.Field()
    h_volumnCOIN = scrapy.Field()
    i_circulatingSupply = scrapy.Field()
    k_imageChart = scrapy.Field()