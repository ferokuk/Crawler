import scrapy


class MachinistResumeSpider(scrapy.Spider):
    name = 'machinist_resume_spider'
    allowed_domains = ['hh.ru']
    start_urls = ['http://hh.ru/']
    pages_count = 250
    
    def start_requests(self):
        for i in range(0, self.pages_count):
            url_machinist = f"https://hh.ru/search/resume?text=%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%B8%D1%81%D1%82&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&page={i}&hhtmFrom=resume_search_result"
            yield scrapy.Request(url_machinist,callback=self.parse_pages)

    def parse_pages(self, response):
        for link in response.css("a.serp-item__title::attr(href)").extract():
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        position = response.css("span.resume-block__title-text::text").get()

        if "машинист" not in position.lower():
            return

        specs = response.css("li.resume-block__specialization::text").get()
        resume = {
            "Position": position,
            "Specializations": specs,
            "Link": response.request.url
        }
        yield resume
