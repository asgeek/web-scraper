from framework.website.WebSite import WebSite
from extensions.MedianProcessor import MedianProcessor
from framework.util.logger.Log import Log
from framework.util.project.Project import Project
from framework.data.persistence.CSV import CSV, SourceType
import datetime
import csv
import re


class RealestateRent(WebSite):
    ad_urls = []
    csv_file_name = 'rent-medians'
    csv_headers = ['Region', 'Suburb', '1 Bed Unit Median', '2 Bed Unit Median', '3 Bed Unit Median',
                   '2 Bed House Median',
                   '3 Bed House Median', '4 Bed House Median', '5 Bed House Median']
    collection_name = 'rent-ads'

    def __init__(self):
        self.set_web_name('realestatecomau')
        self.set_root_url('https://www.realestate.com.au')
        self.set_pagination_pattern('/list-{0}')

    def scrape_ads(self):
        ad_type_list = self.generate_ad_types('suburbs-rent')

        csv_output = CSV(self.csv_file_name, SourceType.OUTPUT)
        csv_output.create_new_and_backup_old()
        csv_output.set_header(self.csv_headers)

        for ad_type in ad_type_list:
            # ad_type.to_string()
            ad_list_pages = ad_type.generate_ad_list_pages("//article[contains(@class, 'tier1')]//a[@class='detailsButton']/@href")
            for ad_list_page in ad_list_pages:
                ads = ad_list_page.read_ads()
                for ad in ads:
                    ad.make_ad_object('_id', ad.ad_url)
                    ad.make_ad_object('ad-url', ad.ad_url)
                    ad.make_ad_object('region', ad_type.ad_type_details['region'])
                    ad.make_ad_object('suburb', ad_type.ad_type_details['suburb'])
                    ad.make_ad_object('postal-code', ad_type.ad_type_details['postal code'])
                    ad.make_ad_object('type', ad.read_content(
                        "//div[@class='featureListWrapper']/div[@class='featureList']/ul[1]/li[2]/span/text()"))
                    ad.make_ad_object('no-of-beds', ad.read_content(
                        "//div[@class='featureListWrapper']/div[@class='featureList']/ul[1]/li[3]/span/text()"))

                    price = ad.read_content("//p[@class='priceText']/text()")
                    formatted_price = self.format_price(price)
                    Log.debug('Formatted Price : {0}'.format(formatted_price))
                    ad.make_ad_object('price', formatted_price)

                    ad.to_string()
                    ad.save_ad(self.collection_name)

            data_set = []
            meproc = MedianProcessor(self.collection_name, ad_type.ad_type_details['region'], ad_type.ad_type_details['suburb'],
                                     ad_type.ad_type_details['postal code'])
            data_set.append(ad_type.ad_type_details['region'])
            data_set.append(ad_type.ad_type_details['suburb'])
            data_set.append(meproc.find_median('Unit', '1'))
            data_set.append(meproc.find_median('Unit', '2'))
            data_set.append(meproc.find_median('Unit', '3'))
            data_set.append(meproc.find_median('House', '2'))
            data_set.append(meproc.find_median('House', '3'))
            data_set.append(meproc.find_median('House', '4'))
            data_set.append(meproc.find_median('House', '5'))

            csv_output.append_array(data_set)

    # Format the date read from web page to standard datetime
    # def format_ad_date(self, str_date):
    #     date_time = str(date.today().year) + " " + str_date
    #     date_t = str(datetime.strptime(date_time, '%Y %d %b %I:%M %p'))
    #     # Debug
    #     print(date_t)
    #     #
    #     return date_t

    def format_price(self, price):
        Log.debug('Price before formatting : {0}'.format(price))
        price_data = re.search(r'(\$([0-9]+[\.]*[\,]*[\ ]*[0-9]*[k|K]?))', price)
        if price_data:
            price_value = price_data.group(0)
            price_int = ''.join(re.findall(r'\d+', price_value))
            Log.debug('Price after formatting : {0}'.format(price_int))
            if re.search(r'([k|K]$)', price_value):
                price_int = price_int * 1000
                return price_int
            elif re.search(r'([m|M]$)', price_value):
                price_int = price_int * 1000000
                return price_int
            else:
                return price_int
        else:
            return 'n/a'
