from framework.util.logger.Log import Log
from lxml import html
import requests
import gc


class Scraper:

    url = ''
    html_page = ''

    def __init__(self, url):
        self.url = url
        self.get_html_page()

    def get_html_page(self):
        try:
            page = requests.get(self.url)
            self.html_page = html.fromstring(page.content)
        except Exception as excep:
            Log.fatal(excep)
            exit(1)

    def read_properties(self, expression):
        properties = self.html_page.xpath(expression)
        return properties

    def clean_scraper(self):
        del self.html_page
        gc.collect()
