import scrapy
import json


class JobsSpider(scrapy.Spider):
    name = "Jobs"
    domains = "https://www.infojobs.com.br"
    search = "/empregos.aspx?palabra=python"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"}     

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
                method="get",
                headers=self.headers,
                callback=self.collecting_data
            )

    def collecting_data(self, response):
        path_json = response.xpath('//script[@type="application/ld+json"]/text()').get()
        json_info = json.loads(path_json)

        job_data = {
            "title": json_info["title"],
            "company_name": json_info["hiringOrganization"]["name"],
            "location": json_info["jobLocation"]["address"]["addressLocality"],
            "min_salary": json_info["baseSalary"]["value"]["minValue"],
            "max_salary": json_info["baseSalary"]["value"]["maxValue"],
            "type_work":  response.xpath('//div[@class="js_applyVacancyHidden js_visibleWhileKillers"   ]/div[2]/div[@class="text-medium small font-weight-bold mb-4"]/text()').getall()[1].replace("\r\n\r\n","").strip(),
            "description": json_info["description"]
        }   

        print(job_data)

