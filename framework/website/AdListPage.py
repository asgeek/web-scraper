from framework.website.Ad import Ad
from framework.scraper.Scraper import Scraper
from framework.util.logger.Log import Log


class AdListPage:
    # properties
    ad_url_list = []
    page_url = ''
    scraper = ''
    ad_url_xpath = ''

    # Relationship one:AdType
    ad_type = ''

    def __init__(self, ad_type_url, ad_url_xpath, ad_type):
        self.page_url = ad_type_url
        self.ad_type = ad_type
        self.ad_url_xpath = ad_url_xpath
        self.scraper = Scraper(self.page_url)
        self.read_ad_urls(ad_url_xpath)

    def read_ad_urls(self, ad_url_xpath):
        # read ad url list from ad list page on website
        ad_list = self.scraper.read_properties(ad_url_xpath)
        self.ad_url_list = ad_list

    def is_ad_list_page(self):
        if not self.ad_url_list:
            return False
        else:
            return True

    def get_first_ad_url(self):
        try:
            return self.ad_url_list[0]
        except:
            return 0

    def create_full_url(self, ad_url):
        if ad_url[:4] == 'http':
            return ad_url
        else:
            return self.ad_type.web_site.root_url + ad_url

    def read_ads(self):
        for ad_url in self.ad_url_list:
            # TODO: Add more control options like Date Range, etc
            if ad_url != self.ad_type.last_ad_url:
                full_ad_url = self.create_full_url(ad_url)
                Log.info('Reading Ad: {0} ...'.format(full_ad_url))
                ad = Ad(full_ad_url, self)
                yield ad
            else:
                Log.info('Met the last Ad URL!')
                raise StopIteration

    def to_string(self):
        Log.info('Ad Page: ' + self.page_url)
