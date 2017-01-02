import scrapy, re
from scrapy.http import HtmlResponse
from scrapy.selector import Selector


with open('apsjobs_search_results.html') as f:
    body = f.read()

rows = Selector(text=body).css('#ctl00_ContentPlaceHolderSite_lvSearchResults_gvListView').css('.item, .altItem').extract()
print('Rows: {}'.format(len(rows)))

for i, row in enumerate(rows):
    id = re.search('Notices=([0-9]*)', Selector(text=row).css('td:nth-child(2)').css('a::attr(href)').extract_first()).group(1)
    url = Selector(text=row).css('td:nth-child(2)').css('a::attr(href)').extract()[-1]
    date = Selector(text=row).css('td:nth-child(3)::text').extract_first().split(':')[-1].strip()
    print('ID: {} | URL: www.apsjobs.gov.au/{} | DATE: {}'.format(id, url, date ))
