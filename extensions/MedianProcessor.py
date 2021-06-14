from statistics import StatisticsError
from statistics import median

from framework.data.persistence.MongoDB import MongoDB
from framework.util.logger.Log import Log


class MedianProcessor:
    suburb = ''
    region = ''
    postal_code = ''
    collection_name = ''

    def __init__(self, collection_name, region, suburb, postal_code):
        self.collection_name = collection_name
        self.region = region
        self.suburb = suburb
        self.postal_code = postal_code

    def get_price_list(self, item_type, no_of_beds):
        db = MongoDB()
        query = {'type': item_type, 'no-of-beds': no_of_beds, 'suburb': self.suburb, 'region': self.region,
                 'postal-code': self.postal_code, 'price': {'$ne': 'n/a'}}
        no_of_items = db.find_count(self.collection_name, query)
        items = db.find_many(self.collection_name, query)
        prices = []
        for item in items:
            price = float(item['price'])
            Log.debug('Price of house: {0}'.format(price))
            prices.append(price)
        return prices

    def find_median(self, item_type, no_of_beds):
        price_list = self.get_price_list(item_type, no_of_beds)
        try:
            median_price = median(price_list)
            Log.info('{0} - {1} beds Median: {2}'.format(item_type, no_of_beds, median_price))
            return median_price
        except StatisticsError:
            return 'N/A'
