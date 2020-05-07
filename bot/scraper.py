from typing import List

from selenium.webdriver import Chrome, ChromeOptions

from .item import RestockedItem


class Scraper:
    def __init__(self, driver):
        self.d = driver

    @staticmethod
    def get_reusable_driver():
        opts = ChromeOptions()

        # Disable images
        prefs = {"profile.managed_default_content_settings.images": 2}
        opts.add_experimental_option("prefs", prefs)

        return Chrome(options=opts)

    def get_restocked(self) -> List[RestockedItem]:
        raise NotImplementedError


class SupremeScraper(Scraper):
    def get_restocked(self):
        return [RestockedItem('test')]