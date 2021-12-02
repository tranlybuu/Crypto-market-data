import scrapy
from ..items import CryptoItem
from datetime import datetime
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from scrapy.utils.project import get_project_settings

class CryptoBotSpider(scrapy.Spider):
    name = 'crypto_bot1'
    
    def start_requests(self):
        list_url = []
        for item in range(1,2):
            url = 'https://www.coingecko.com/vi?page=' + str(item)
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
        
        count_rank = response.xpath('//table/tbody').extract()
        count_rank = str(count_rank)
        count_rank = count_rank.replace("<tr>","*")
        count = 0
        for item in count_rank:
            if item == "~":
                count+=1
        for x in range(1,count+1):
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            time = now.strftime("%H:%M:%S")
            rank = response.xpath(f'//tbody/tr[{x}]/td[2]/text()').get()
            name = response.xpath(f'//tbody/tr[{x}]/td[3]/div/div[2]/a/text()').get()
            symbol = response.xpath(f'//tbody/tr[{x}]/td[3]/div/div[2]/a[2]/text()').get()
            price = response.xpath(f'//tbody/tr[{x}]/td[4]/span/text()').get()
            P24h = response.xpath(f'//tbody/tr[{x}]/td[6]/span').get()
            P7d = response.xpath(f'//tbody/tr[{x}]/td[7]/span').get()
            marketCap = response.xpath(f'//tbody/tr[{x}]/td[8]/span/text()').get()
            volumnUSD = response.xpath(f'//tbody/tr[{x}]/td[9]/span/text()').get()
            circulatingSupply = ""
            imageChart = response.xpath(f'//tbody/tr[{x}]/td[10]/a/img/@src').extract()
            ###################
            """ P24h = <span class="sc-15yy2pl-0 kAXKAX"><span class="icon-Caret-up"></span>1.27<!-- -->%</span> """
            edit = str(P24h)
            if 'span class="text-green"' in edit:
                P24h = "+" + str(response.xpath(f'//tbody/tr[{x}]/td[6]/span/text()').get())
            elif 'span class="text-danger"' in edit:
                P24h = "-" + str(response.xpath(f'//tbody/tr[{x}]/td[6]/span/text()').get())
            else:
                P24h = "#" + str(response.xpath(f'//tbody/tr[{x}]/td[6]/span/text()').get())
            """ P7d = <span class="sc-15yy2pl-0 kAXKAX"><span class="icon-Caret-up"></span>5.50<!-- -->%</span> """
            edit = str(P7d)
            if 'span class="text-green"' in edit:
                P7d = "+" + str(response.xpath(f'//tbody/tr[{x}]/td[7]/span/text()').get())
            elif 'span class="text-danger"' in edit:
                P7d = "-" + str(response.xpath(f'//tbody/tr[{x}]/td[7]/span/text()').get())
            else:
                P7d = "#" + str(response.xpath(f'//tbody/tr[{x}]/td[7]/span/text()').get())
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
