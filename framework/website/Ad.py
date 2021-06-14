from framework.data.persistence.MongoDB import MongoDB
from framework.scraper.Scraper import Scraper
from framework.util.logger.Log import Log


class Ad:

    ad_json = ''
    scraper = ''
    ad_object = {}

    # relationship one:AdListPage
    ad_list_page = ''

    def __init__(self, ad_url, ad_list_page):
        self.ad_url = ad_url
        self.ad_list_page = ad_list_page
        self.scraper = Scraper(ad_url)

    def read_content(self, xpath):
        content = self.scraper.read_properties(xpath)
        content_value = self.get_value_at(content, 0)
        Log.debug('Content : {0}'.format(content_value))
        return content_value

    def read_content_list(self, xpath):
        content = self.scraper.read_properties(xpath)
        return content

    def make_ad_object(self, attr_name, attr_value):
        self.ad_object[attr_name] = attr_value

    def get_value_at(self, value_array, index):
        try:
            return value_array[index]
        except IndexError:
            return ''

    def save_ad(self, collection_name):
        db = MongoDB()
        ad_id = db.insert_one(collection_name, self.ad_object)
        return ad_id

    def to_string(self):
        Log.info(self.ad_object)
