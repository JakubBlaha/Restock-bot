from typing import List

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .item import RestockedItem
from .config import conf


class Scraper:
    def __init__(self, driver: Chrome):
        self.d = driver

    @staticmethod
    def get_reusable_driver():
        opts = ChromeOptions()

        # Disable images
        prefs = {"profile.managed_default_content_settings.images": 2}
        opts.add_experimental_option("prefs", prefs)

        # Headless
        if conf['headless'] == 'True':
            opts.add_argument('headless')

        return Chrome(options=opts)

    def get_restocked(self) -> List[RestockedItem]:
        raise NotImplementedError


class SupremeScraper(Scraper):
    def get_restocked(self, ignored):
        self.d.get('https://www.supremecommunity.com/restocks/us/1/')

        name_tags = self.d.find_elements_by_class_name('restock-name')

        names = [i.get_attribute('innerText') for i in name_tags]
        colorways = [i.get_attribute('innerText') for i in self.d.find_elements_by_class_name('restock-colorway')]
        dts = [i.get_attribute('datetime') for i in self.d.find_elements_by_class_name('timeago')]
        images = [i.get_attribute('src') for i in self.d.find_elements_by_class_name('size-thumbnail')]

        items = []

        ignored = [i.title + i.description + i.dt for i in ignored]

        for name_tag, name, colorway, dt, img, in zip(name_tags, names, colorways, dts, images):
            item = RestockedItem(name, colorway, dt, img, None, None)

            if item.title + item.description + item.dt in ignored:
                continue

            # name_tag.click()

            # self.d.switch_to.window(self.d.window_handles[-1])

            # item.url = self.d.current_url
            # item.price = WebDriverWait(self.d, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'price'))).get_attribute('innerText')

            # self.d.close()
            # self.d.switch_to.window(self.d.window_handles[0])

            items.append(item)

        return items
