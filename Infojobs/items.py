import scrapy


class InfojobsItem(scrapy.Item):
    title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    type_work = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    description = scrapy.Field()
    
