import scrapy

class CooksSpider(scrapy.Spider):
    name = 'cooks_spider'
    allowed_domains = ['hh.ru']
    start_urls = ['http://hh.ru/']
    pages_count = 15
    id = -1
    def start_requests(self):
        for i in range(10, self.pages_count ):
            url_cook = f"https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=%D0%BF%D0%BE%D0%B2%D0%B0%D1%80&page={i}&hhtmFrom=vacancy_search_list"
            yield scrapy.Request(url_cook, callback=self.parse_pages)
        
    def parse_pages(self, response):
        for link in response.css("a.serp-item__title::attr(href)").extract():
            url = response.urljoin(link)
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        position = response.css("h1.bloko-header-section-1::text").get().replace(",","")

        if "повар" not in position.lower():
            return
            
        info = "".join(response.css("p::text").getall()[:-17:])
        info += "".join(str(i+1)+ ") "+ n+"\n" for i,n in enumerate(response.css("li::text").getall()) if n != "Уведомления в мессенджер") + "\n"
        self.id += 1
        yield {
            "ID": self.id,
            "Position": position,
            "Specializations": info.replace(","," "),
            "Link": response.request.url
        }
    
        
