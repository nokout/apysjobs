import re, arrow
from scrapy.selector import Selector
from bs4 import BeautifulSoup

def build_object(body, notice={}):
    notice['notice_type_text'] = Selector(text=body).css('.noticeType::text').extract_first().strip()
    notice['portfolio'] = Selector(text=body).css('#ctl00_c_ucNoticeDetails_tdPortfolio::text').extract_first().strip()
    notice['agency'] = Selector(text=body).css('.agency::text').extract_first().strip()
    notice['closing_date_string'] = Selector(text=body).css('.closingDate::text').extract_first().split(':')[-1].strip()
    notice['closing_date_formatted'] =  arrow.get(notice['closing_date_string'], 'dddd, D MMMM YYYY').format('YYYY/MM/DD')
    # print('as arrow date: {}'.format(closing_date_arrow))
    # print('as formatted date: {}'.format(closing_date_arrow.format('YYYY/MM/DD')))

    notice['job_title'] = Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrPositionTitle').css('td:nth-child(2)::text').extract_first().strip()
    notice['branch'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrBranch').css('td:nth-child(2)::text').extract_first()).strip()
    notice['section'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrSection').css('td:nth-child(2)::text').extract_first()).strip()
    notice['job_type'] = [x.strip() for x in Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrPositionType').css('td:nth-child(2)::text').extract_first().split(',')]
    notice['salary_text'] = Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrSalary').css('td:nth-child(2)::text').extract_first()
    if notice['salary_text']:
        notice['salary_min'] = notice['salary_text'].split('-')[0].replace('$','').replace(',','').strip()
        notice['salary_max'] = notice['salary_text'].split('-')[-1].replace('$','').replace(',','').strip()
    notice['locations_text'] = Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_ucToClassificationsLabel_tbrLocation').css('td:nth-child(2)::text').extract_first()
    notice["locations"] = []
    for location in notice['locations_text'].split(';'):
          if location.find(" - ") >= 0:
              notice['locations'].append({'state': location.split('-')[1].strip(), 'city': location.split('-')[0].strip()})
          else:
              notice['locations'].append({'other': location})

    notice['classification_text'] = Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_ucToClassificationsLabel_tbrClassification').css('td:nth-child(2)::text').extract_first()
    notice['broadband_classification_text'] = Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_ucToClassificationsLabel_tbrBroadband').css('td:nth-child(2)::text').extract_first()
    if notice['classification_text']:
        notice['classifications'] = [x.strip() for x in notice['classification_text'].split(',')]
    elif notice['broadband_classification_text']:
        notice['classifications'] = [x.strip() for x in notice['broadband_classification_text'].split(',')]

    notice['employment_act'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_ucToClassificationsLabel_tbrAgencyAct::text').extract_first()).strip()
    notice['position_id'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrPositionNo').css('td:nth-child(2)::text').extract_first()).strip()
    notice['agency_website'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrAgencyUrlTop').css('td:nth-child(2) a::attr(href)').extract_first()).strip()
    if len(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrAmendments span::text').extract()) > 0:
        notice['amendments'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrAmendments span::text').extract()[-1]).strip()

    notice['selection_documentation'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrSelectionDocumentation').css('td:nth-child(2)::text').extract_first()).strip()
    notice['position_contact'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrContactDetails').css('td:nth-child(2)::text').extract_first()).strip()
    notice['position_contact_address'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrApplyText').css('td:nth-child(2)::text').extract_first()).strip()
    notice['agency_website_recruitment'] = Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_tbrAgencyRecruitmentUrl').css('td:nth-child(2)::text').extract_first().strip()
    notice['agency_website_apply_function_text'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_lnkApply::attr(onclick)').extract_first()).strip()
    notice['agency_website_information'] = str(Selector(text=body).css('#ctl00_c_ucNoticeDetails_ucNoticeView_lnkAgencyRecruitment::attr(href)').extract_first()).strip()
    notice['notes_html'] = Selector(text=body).css('#ctl00_c_ucNoticeDetails_pnlNotes > div.notes').extract()

    # In order to extract the position description it needs to be seperated from the other content
    # in the viewContent div. This is done in beautiful Soup.
    view_content = Selector(text=body).css("#viewContent").extract_first()
    soup = BeautifulSoup(view_content, "lxml")
    # remove the inner table conent which contains all the information we have already extracted
    [x.extract() for x in soup.find_all(class_ = 'innerTable')]
    [x.extract() for x in soup.find_all(id = 'ctl00_c_ucNoticeDetails_ucNoticeView_tbrAmendments')]

    notice['position_description_html'] = re.sub('\<h2\>\s*To Apply\s*\<\/h2\>', '', unicode(soup.prettify()))

    return notice


if __name__ == "__main__":
    import json

    with open('test_assets/1.html') as f:
        result = build_object(f.read())
        print(json.dumps(result, indent=3))
        # closing_date_string = result['closing_date_string']
        # print('closing_date_string: {}'.format(closing_date_string))
        # # Date Example: Thursday, 26 January 2017
        # closing_date_arrow =  arrow.get(closing_date_string, 'dddd, D MMMM YYYY')
        # print('as arrow date: {}'.format(closing_date_arrow))
        # print('as formatted date: {}'.format(closing_date_arrow.format('YYYY/MM/DD')))
