import abc
from framework.website.AdType import AdType
from framework.util.logger.Log import Log
from framework.data.persistence.CSV import CSV, SourceType


class WebSite:
    __metaclass__ = abc.ABCMeta

    # properties
    web_name = ''
    root_url = ''
    pagination_pattern = ''

    def set_web_name(self, web_name):
        Log.info('Web Name : {0}'.format(web_name))
        self.web_name = web_name

    def get_web_name(self):
        return self.web_name

    def set_root_url(self, root_url):
        Log.debug('Root URL : {0}'.format(root_url))
        self.root_url = root_url

    def get_root_url(self):
        return self.root_url

    def set_pagination_pattern(self, pagination_pattern):
        Log.debug('Pagination Pattern : {0}'.format(pagination_pattern))
        self.pagination_pattern = pagination_pattern

    def get_pagination_pattern(self):
        return self.pagination_pattern

    def generate_ad_types(self, input_file_name):
        ad_type_list = self.load_csv_ad_type_list(input_file_name)
        first = True
        for ad_type in ad_type_list:
            Log.debug('Ad Type Name : {0}'.format(ad_type))
            Log.debug('Ad Tyoe URL : {0}'.format(ad_type['url']))
            Log.debug('Pagination Pattern {0}'.format(self.pagination_pattern))
            ad_type = AdType(ad_type, ad_type['url'].format(self.pagination_pattern), self)
            yield ad_type

    def load_csv_ad_type_list(self, file_name):
        list_file = CSV('suburbs-rent', SourceType.INPUT)
        return list_file.read_file()

    def to_string(self):
        Log.info('Web Name : ' + self.web_name)
        Log.info('Root URL : ' + self.root_url)
        Log.info('Pagination Pattern : ' + self.pagination_pattern)

