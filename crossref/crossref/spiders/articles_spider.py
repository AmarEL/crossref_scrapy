import scrapy
import urllib.parse


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    default_url = 'https://api.crossref.org/works?query=Ecosystem+Services&filter=type:other,' \
                  'from-pub-date:2014-03-03&rows=500&cursor='
    start_urls = [
        default_url + '*'
    ]

    def parse(self, response):
        json_response = response.json()
        next_cursor = json_response['message']['next-cursor']
        if next_cursor:
            yield scrapy.Request(self.default_url + urllib.parse.quote_plus(next_cursor), callback=self.parse, encoding='ascii')

        for item in json_response['message']['items']:
            yield {'article': item}
