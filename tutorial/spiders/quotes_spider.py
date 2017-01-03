import scrapy
import re
import json
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from build_object import build_object


class QuotesSpider(scrapy.Spider):
    name = "apsjobs"
    notices = {}
    custom_settings = {
        'COOKIES_ENABLED': True
    }

    def start_requests(self):

        # This initial request basically just sets up the session
        #   and page size before we do the search.
        yield scrapy.Request(
            url="""https://www.apsjobs.gov.au/quickSearch.aspx?mn=JobSearch&ifm=true""",
            callback=self.setup_parse,
            cookies={'UserPreferencesPageSize': "PageSize=1000"})

    def setup_parse(self, response):
        headers = {
            'Host': 'www.apsjobs.gov.au',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.apsjobs.gov.au/quickSearch.aspx?mn=JobSearch&ifm=true',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            '__SCROLLPOSITIONX': '400',
            '__SCROLLPOSITIONY': '119',
            '__VIEWSTATEENCRYPTED': '',
            'ctl00$ContentPlaceHolderSite$ucAgency': '',
            'ctl00$ContentPlaceHolderSite$ucJobCategory': '',
            'ctl00$ContentPlaceHolderSite$ucClassification': '',
            'ctl00$ContentPlaceHolderSite$ucState': '',
            'ctl00$ContentPlaceHolderSite$txtKeywords': '',
            'ctl00$ContentPlaceHolderSite$txtMinSalary': '',
            'ctl00$ContentPlaceHolderSite$txtMaxSalary': '',
            'ctl00$ContentPlaceHolderSite$btnSearch': 'Search',
            'ctl00$ContentPlaceHolderSite$hMessage': ''
        }

        # TODO Put cookies in construction and change to a yield instead of
        # return
        main_request = scrapy.http.FormRequest.from_response(response,
                                                             formname="aspnetForm",
                                                             formdata=data,
                                                             headers=headers,
                                                             # url='''https://www.apsjobs.gov.au/quickSearch.aspx?mn=JobSearch&ifm=true''',
                                                             clickdata={
                                                                 'name': 'ctl00$ContentPlaceHolderSite$btnSearch'},
                                                             callback=self.get_search_results)

        main_request.cookies['UserPreferencesPageSize'] = "PageSize=1000"

        return [main_request]

    def get_search_results(self, response):

        if response.status != 200:
            self.error('Non 200 result')

        self.log("Status: {}".format(response.status))
        self.log("Headers: {}".format(response.headers))
        self.log("Flags: {}".format(response.flags))
        #
        # page = response.url.split("/")[-2]
        # filename = 'apsjobs_search_results.html'.format(page)
        # with open(filename, 'wb') as f:

        #     f.write(response.body)
        # self.log('Saved file {}'.format(filename))
        with open('search_result.html', 'wb') as f:
            f.write(response.body)

        rows = Selector(response=response).css(
            '#ctl00_ContentPlaceHolderSite_lvSearchResults_gvListView').css('.item, .altItem').extract()
        self.log('Notices Found: {}'.format(len(rows)))
        for i, row in enumerate(rows):
            url = response.urljoin(Selector(text=row).css(
                'td:nth-child(2)').css('a::attr(href)').extract()[-1])
            id = re.search('Notices=([0-9]*)', Selector(text=row).css(
                'td:nth-child(2)').css('a::attr(href)').extract_first()).group(1)
            date = Selector(text=row).css('td:nth-child(3)::text').extract_first().split(':')[-1]
            self.notices['id'] = {'notice_id': id, 'notice_url': url, 'notice_publish_date': date}

            yield scrapy.Request(response.urljoin(url), callback=self.parse)

            if i > 3:
                break

    def parse(self, response):
        id = re.search('Notices=([0-9]*)', response.url).group(1)

        with open('''output/{}.html'''.format(id), 'wb') as f:
            f.write(response.body)

        with open('''output/{}.json'''.format(id), 'w') as f:
            notice_doc = build_object(response.body, self.notices['id'])
            f.write(json.dumps(notice_doc, indent=4))
            # TODO write to elastic search
