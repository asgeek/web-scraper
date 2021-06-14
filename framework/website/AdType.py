from framework.website.AdListPage import AdListPage
from framework.util.logger.Log import Log
# from framework.database.Database import *


class AdType:
    # properties
    ad_type_details = {}
    ad_type_url = ''
    last_ad_url = ''
    page_number = 0
    first_ad_url = ''

    # Relationship one:WebSite
    web_site = ''

    def __init__(self, ad_type_details, ad_type_url, web_site):
        Log.info('Ad Type Name : {0}'.format(ad_type_details))
        self.ad_type_details = ad_type_details
        Log.info('Ad Type URL : {0}'.format(ad_type_url))
        self.ad_type_url = ad_type_url
        self.web_site = web_site

    # there should be many possible ways to scrape data from a site
    # as an example:
    #   - 1. start from where the scraper stops at last time ie. from the last scraped item onwards
    #   - 2. scrape all items
    #   - 3. scrape items within a date range
    #   - 4. scrape items within a ID rang
    #   - etc
    # for the moment, I will create scrape all items (2nd) method
    # other methods needed to be created in future as the needed
    # 1st method is created to find the last saved item from a mysql db as in below method.
    # it needs to be converted to find last saved item from MongoDB db
    # so I will comment it out for the moment.

    # query the last element from the DB and return it
    # def set_last_ad_url(self):
    #     # last_element = '/en/ad/toyota-coaster-2006-for-sale-colombo-53'
    #     db = Database()
    #     last_ad = db.execute_select("SELECT ad_url, datetime "
    #                                 "FROM ad "
    #                                 "WHERE category = '{0}' "
    #                                 "ORDER BY sort_key DESC LIMIT 1;".format(self.ad_type_name))
    #     try:
    #         self.last_ad_url = last_ad[0][0]
    #     except:
    #         self.last_ad_url = 'nan'

    def set_first_ad_url(self, first_ad_url):
        self.first_ad_url = first_ad_url

    def generate_ad_list_pages(self, ad_url_xpath):
        page_number = 1
        while True:
            page_url = self.ad_type_url.format(page_number)
            Log.info('Page URL : {0}'.format(page_url))
            ad_list_page = AdListPage(page_url, ad_url_xpath, self)
            # save 1st ad in 1st page to eliminate duplicate pages
            if page_number == 1:
                self.first_ad_url = ad_list_page.get_first_ad_url()
            Log.debug('First Ad URL: {0}'.format(self.first_ad_url))
            Log.debug('New Page First Ad URL: {0}'.format(ad_list_page.get_first_ad_url()))
            if not ad_list_page.is_ad_list_page():
                raise StopIteration
            elif self.first_ad_url == ad_list_page.get_first_ad_url() and page_number != 1:
                raise StopIteration
            else:
                yield ad_list_page
                page_number += 1

    def to_string(self):
        # should be logging
        # Log.info('Ad Type Details : ' + self.ad_type_details)
        Log.info('Ad Type URL : ' + self.ad_type_url)
        Log.info('Last Ad URL : ' + self.last_ad_url)
