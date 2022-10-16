# Crawler
A simple task with Scrapy Python library to parse hh.ru resumes.


If you want to run script:

1) clone repo

2) run "pip install -r requirements.txt"

3) run "scrapy crawl cooks_spider -O c.json" to get all visible cook resumes

4) run "scrapy crawl machinists_spider -O m.json" to get all visible machinist resumes

5) run "python json_fix.py" to get 2 result files with all vacancies
