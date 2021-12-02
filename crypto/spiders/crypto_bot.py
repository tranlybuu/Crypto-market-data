import scrapy
from ..items import CryptoItem
from datetime import datetime
from scrapy_selenium import SeleniumRequest

class CryptoBotSpider(scrapy.Spider):
    name = 'crypto_bot'

    def start_requests(self):
        list_url = []
        for item in range(1,2):
            url = 'https://coinmarketcap.com/?page=' + str(item)
            list_url.append(url)
        for item in list_url:
            yield SeleniumRequest(
                url = item,
                wait_time = 3,
                screenshot = True,
                callback = self.parse,
                script='window.scrollTo(0, document.body.scrollHeight);',
                dont_filter = True
            )

    def parse(self, response):
        
        count_rank = response.xpath('//tbody').extract()
        count_rank = str(count_rank)
        count_rank = count_rank.replace("<tr>","~")
        count = 0
        for item in count_rank:
            if item == "~":
                count+=1
        for x in range(1,count+1):
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            time = now.strftime("%H:%M:%S")
            rank = response.xpath(f'//tbody/tr[{x}]/td[2]/p/text()').get()
            name = response.xpath(f'//tbody/tr[{x}]/td[3]/div/a/div/div/p/text()').get()
            symbol = response.xpath(f'//tbody/tr[{x}]/td[3]/div/a/div/div/div/p/text()').get()
            price = response.xpath(f'//tbody/tr[{x}]/td[4]/div/a/span/text()').get()
            P24h = response.xpath(f'//tbody/tr[{x}]/td[5]/span').get()
            P7d = response.xpath(f'//tbody/tr[{x}]/td[6]/span').get()
            marketCap = response.xpath(f'//tbody/tr[{x}]/td[7]/p/span[2]/text()').get()
            volumnUSD = response.xpath(f'//tbody/tr[{x}]/td[8]/div/a/p/text()').get()
            volumnCOIN = response.xpath(f'//tbody/tr[{x}]/td[8]/div/p/text()').get()
            circulatingSupply = response.xpath(f'//tbody/tr[{x}]/td[9]/div/div/p/text()').get()
            imageChart = response.xpath(f'//tbody/tr[{x}]/td[10]/a/img/@src').extract()
            """ P24h = <span class="sc-15yy2pl-0 kAXKAX"><span class="icon-Caret-up"></span>1.27<!-- -->%</span> """
            edit = str(P24h)
            index = edit.index("!")
            if "Caret-up" in edit:
                P24h = "+" + edit[(index-5):(index-1)] + "%"
            elif "Caret-down" in edit:
                P24h = "-" + edit[(index-5):(index-1)] + "%"
            else:
                P24h = "#" + edit[(index-5):(index-1)] + "%"
            """ P7d = <span class="sc-15yy2pl-0 kAXKAX"><span class="icon-Caret-up"></span>5.50<!-- -->%</span> """
            edit = str(P7d)
            index = edit.index("!")
            if "Caret-up" in edit:
                P7d = "+" + edit[(index-5):(index-1)] + "%"
            elif "Caret-down" in edit:
                P7d = "-" + edit[(index-5):(index-1)] + "%"
            else:
                P7d = "#" + edit[(index-5):(index-1)] + "%"
            ##################
            item = CryptoItem()
            item["a_DT_date"] = date
            item["a_DT_time"] = time
            item["a_rank"] = rank
            item["b_name"] = name
            item["c_symbol"] = symbol
            item["d_price"] = price
            item["e_P24h"] = P24h
            item["f_P7d"] = P7d
            item["g_marketCap"] = marketCap
            item["h_volumnUSD"] = volumnUSD
            item["h_volumnCOIN"] = volumnCOIN
            item["i_circulatingSupply"] = circulatingSupply
            item["k_imageChart"] = imageChart
            yield item
