import scrapy
import time
import re
class MachinistResumeSpider(scrapy.Spider):
    name = 'machinist_spider'
    allowed_domains = ['hh.ru']    
    handle_httpstatus_all = True
    start_urls = ['http://hh.ru/']
    def start_requests(self):
        start = time.time()
        for i in range(0, 200):
            url = f"https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%B8%D1%81%D1%82&items_on_page=10&page={i}"
            yield scrapy.Request(url, callback=self.parse_pages)
        end = time.time()
        print(f"[+] Total time was: {round((end-start)/60)} min.")
    def parse_pages(self, response):
        for link in response.css("a.serp-item__title::attr(href)").extract():
            url = response.urljoin(link)
            yield scrapy.Request(url,callback=self.parse)
    def parse(self, response):
        position = response.css("h1.bloko-header-section-1::text").get()
        if "машинист" not in str(position).lower():
            return
        id = (str(response.request.url).split("/"))[4].split("?")[0]
        salry =''.join((response.css("div.vacancy-title  ::text").extract())[1::])

        title_info_exp = response.css("p.vacancy-description-list-item ::text").extract()

        dct = {
                "Required_work_exp" : title_info_exp[2],
                "Other_info": ''.join(title_info_exp[3:])
            }
        
        info_from_p = response.css("div.g-user-content p::text").extract()
        info_from_ul = response.css("div.g-user-content ul ").extract()

        res = []
        info = []
        
        for i in range(len(info_from_p)-1, -1, -1): 
            if len(info_from_p[i]) < 3 or info_from_p[i][-1] == ":":
                continue
            info.append(info_from_p[i])

        for i in info_from_ul:
            i = i[5:-6].replace("</li>", "*")
            i = i[4:-6].replace("* <li>", "**")
            i = i.split("**")
            res_ul = []
            for j in i:
                if len(j) < 3:
                    continue
                res_ul.append(j)
            if len(res_ul) > 0:
                res.append(self.cleaner(res_ul))

        info_from_p = response.css("div.bloko-tag-list ::text").extract()
        if len(info_from_p) > 0:
            res.append(info_from_p)

        item = {
            "ID": id,
            "Salary" : salry,
            "Position": position,
            "Base_info": dct,
            "Content": res,
            "Link": response.request.url
        }
        with open('m2.json') as f:
            if item["ID"] in f.read():
                return
        yield item

    def cleaner(self, info):
        for i in range(len(info)-1, -1, -1):  
            info[i] = info[i].strip()
            info[i] = re.sub(r'\w+[>]\s?','',info[i]).replace("</", "").replace("<", "")
            if not info[i][0].isalnum():
                j = 0
                while not info[i][j].isalnum() or info[i][j].isdigit():
                    info[i] = info[i].replace(info[i][j], "", 1)
                    j+=1
            if not info[i][-1].isalnum():
                j = len(info[i])-1
                while not info[i][j].isalnum():
                    info[i] = info[i].replace(info[i][j], "", 1)
                    j-=1
            info[i] = info[i].strip()
        return info