import scrapy


class ResumeSpiderSpider(scrapy.Spider):
    name = 'cook_resume_spider'
    allowed_domains = ['hh.ru']
    start_urls = ['http://hh.ru/']
    pages_count = 250

    def start_requests(self):
        for i in range(0, self.pages_count):
            url_cook = f"https://hh.ru/search/resume?area=113&relocation=living_or_relocation&gender=unknown&text=%D0%BF%D0%BE%D0%B2%D0%B0%D1%80&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&search_period=0&page={i}&hhtmFrom=resume_search_result"
            yield scrapy.Request(url_cook, callback=self.parse_pages)
        
    def parse_pages(self, response):
        for link in response.css("a.serp-item__title::attr(href)").extract():
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        position = response.css("span.resume-block__title-text::text").get()

        if "Шеф" in position: 
            return
        if "шеф" in position: 
            return
        if "повар" not in position.lower():
            return

        specs = response.css("li.resume-block__specialization::text").get()
        resume = {
            "Position": position,
            "Specializations": specs,
            "Link": response.request.url
        }
        yield resume
