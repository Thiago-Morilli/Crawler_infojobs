import scrapy
import json
from Infojobs.items import InfojobsItem

class JobsSpider(scrapy.Spider):
    name = "Jobs"
    domains = "https://www.infojobs.com.br"
    search = "/empregos.aspx?palabra=python"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"}  
    job_data = {}   

    def start_requests(self):
        yield scrapy.Request(
                url=self.domains + self.search,
                method="GET",
                headers=self.headers,
                callback=self.parse
        )

    def parse(self, response):
        for get_link in response.xpath('//div[@class="d-flex "]/div/a/@href').getall():
            link = self.domains + get_link
            yield scrapy.Request(               
                url=link,
                method="GET",
                headers=self.headers,
                callback=self.collecting_data
            )   

    def collecting_data(self, response):

        path_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if path_json is not None:
          
            json_info = json.loads(path_json)  

            
            self.job_data["title"] = json_info["title"]
            self.job_data["company_name"] = json_info["hiringOrganization"]["name"]
            self.job_data["location"] = json_info["jobLocation"]["address"]["addressLocality"]
            self.job_data["type_work"] =  response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"   ]/div[2]/div[@class="text-medium small font-weight-bold mb-4"]/text()').getall()[1].replace("\r\n\r\n","").strip()
            self.job_data["description"] = json_info["description"]
        
            yield  self.processing_data(response)

        else:
            self.job_data["title"] = response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"]/h2/text()').get()
            self.job_data["company_name"] = response.xpath('//div[@class="h4"]/a/text()').get()
            self.job_data["location"] = response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"   ]/div[2]/div/text()').get().strip()
            self.job_data["type_work"] =  response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"   ]/div[2]/div[@class="text-medium small font-weight-bold mb-4"]/text()').getall()[1].replace("\r\n\r\n","").strip()
            self.job_data["description"] = response.xpath('//div[@class="pt-24 text-medium js_vacancyDataPanels js_applyVacancyHidden"]/p/text()').get().replace("\r\n\r\n","").replace("\r\n•","").replace("\r\n -","")

            yield  self.processing_data(response)

        yield InfojobsItem(
                self.job_data
            )
            
    def processing_data(self, response):

        min_salary = response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"   ]/div[2]/div[2]/text()').get().split()[1]
        if min_salary != "a":
            self.job_data["min_salary"] = min_salary
        else:
            combine_salary =response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"   ]/div[2]/div[2]/text()').get().strip()
            self.job_data["min_salary"] = combine_salary
        
        try:  
            max_salary = response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"   ]/div[2]/div[2]/text()').get().split()[4]
            self.job_data["max_salary"] = max_salary
        except:
            combine_salary =response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"   ]/div[2]/div[2]/text()').get()
            self.job_data["max_salary"] = "Salário a combinar"

            
        print(self.job_data)
        