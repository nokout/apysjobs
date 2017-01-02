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

        request1 = scrapy.Request(
            url="""https://www.apsjobs.gov.au/quickSearch.aspx?mn=JobSearch&ifm=true""",
            callback=self.setup_parse)
        #    formdata=data,
        # #    cookies={'UserPreferencesCookieCheck': 'APSjobs',
        # #             'UserPreferencesPageSize': '1000',
        # #             'APSjobs_Session': 'a4dpg0orukmugpmpdak0wudv'}
        # )

        return [request1]

    def setup_parse(self, response):
        data = {
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            '__SCROLLPOSITIONX': '271',
            '__SCROLLPOSITIONY': '403',
            '__VIEWSTATEENCRYPTED': '',
            'ctl00$ContentPlaceHolderSite$btnSearch': 'Search'
        }

        # url="""https://www.apsjobs.gov.au/quickSearch.aspx?mn=JobSearch&ifm=true""",
        #                                        cookies={'UserPreferencesCookieCheck': 'APSjobs',
        #                                                 'UserPreferencesPageSize': '1000',
        #                                                 'APSjobs_Session': 'vulbbuk55xezodowvzbb01ce'},
        with open('pre_search_result.html', 'wb') as f:
            f.write(response.body)

        yield scrapy.http.FormRequest.from_response(response,
                                                    formname="aspnetForm",
                                                    formdata=data,
                                                    # url='''https://www.apsjobs.gov.au/quickSearch.aspx?mn=JobSearch&ifm=true''',
                                                    clickdata={'name': 'ctl00$ContentPlaceHolderSite$btnSearch'},
                                                    callback=self.get_search_results)
        # main_request

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
            id = re.search('Notices=([0-9]*)', Selector(text=row).css(
                'td:nth-child(2)').css('a::attr(href)').extract_first()).group(1)
            # url = Selector(text=row).css(
            #     'td:nth-child(2)').css('a::attr(href)').extract()[-1]
            # date = Selector(text=row).css('td:nth-child(3)::text').extract_first().split(':')[-1].strip().css(
            # '#ctl00_c_ucNoticeDetails_ucNoticeView_tbrSalary').css('td:nth-child(2)::text').extract_first()
            # self.notices['id'] = {'id': id, 'url': url, 'data,
            # callback=self.parse': d
            yield scrapy.Request(response.urljoin(url), callback=self.parse)

    def parse(self, response):
        filename = re.search('Notices=([0-9]*)', response.url).group(1)
        with open('html/{}.html'.format(filename), 'wb') as f:
            f.write(response.body)

        with open('''./json/{}.json'''.format(filename), 'wb') as f:
            f.write(json.dumps(build_object(body), indent=4))

# notice_type_text = Selector(response=response).css('.noticeType::text').extract_first().strip()
# portfolio = Selector(response=response).css('#ctl00_c_ucNoticeDetails_tdPortfolio::text').extract_first().strip()
# agency = Selector(response=response).css('.agency::text').extract_first().strip()
# closing_date = Selector(response=response).css('.closingDate::text').extract_first().split(':')[-1].strip()
# job_title = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrPositionTitle').css('td:nth-child(2)::text').extract_first().strip()
# branch = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrBranch').css('td:nth-child(2)::text').extract_first().strip()
# section = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrSection').css('td:nth-child(2)::text').extract_first().strip()
# job_type = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrPositionType').css('td:nth-child(2)::text').extract_first().split(',')
# salary_text = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrSalary').css('td:nth-child(2)::text').extract_first()
# salary_min = salary_text.split('-')[0].replace('$','').replace(',','').strip()
# salary_max = salary_text.split('-')[-1].replace('$','').replace(',','').strip()
# locations_text = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_ucToClassificationsLabel_tbrLocation').css('td:nth-child(2)::text').extract_first()
# ##TODO: Split locations
# classification = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_ucToClassificationsLabel_tbrClassification').css('td:nth-child(2)::text').extract_first().strip()
# ##TODO: Split classifications
# employment_act = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_ucToClassificationsLabel_tbrAgencyAct').css('td'#ctl00_c_ucNoticeDetails_ucNoticeView_lnkAgencyRecruitment::attr(href)':nth-child(2)::text').extract_first().strip()
# position_id = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrPositionNo').css('td:nth-child(2)::text').extract_first().strip()
# agency_website = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrAgencyUrlTop').css('td:nth-child(2) a::attr(href)').extract_first().strip()
#
# ##TODO Extract Position Description
# ##     Not all contained in a div, is in same container as innertables
#
# selection_documentation = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrSelectionDocumentation').css('td:nth-child(2)::text').extract_first().strip()
# position_contact = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrContactDetails').css('td:nth-child(2)::text').extract_first().strip()
# agency_website_recruitment = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrAgencyRecruitmentUrl').css('td:nth-child(2)::text').extract_first().strip()
# agency_website_apply_function_text = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_lnkApply::attr(onclick)').extract_first().strip()
# agency_website_information = Selector(response=response).css('#ctl00_c_ucNoticeDetails_ucNoticeView_lnkAgencyRecruitment::attr(href)').extract_first().strip()
# notes_html = Selector(response=response).css('#ctl00_c_ucNoticeDetails_pnlNotes > div.notes').extract()
#
#
#

# self.log('x.Sastrip() for x in ved file
# {}'.format(filename).css('#ctl00_c_ucNoticeDetails_pnlNotes
# div::text').extract()for.css('#ctl00_c_ucNoticeDetails_divStaticEmploymentOpportunityText::text').extract_first().strip()]
