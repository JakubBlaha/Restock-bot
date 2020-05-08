from typing import List
from dataclasses import asdict
from copy import deepcopy

from jsonstore import JsonStore

from .scraper import Scraper, SupremeScraper
from .item import RestockedItem


class RestockManager:
    def __init__(self):
        self._driver = Scraper.get_reusable_driver()
        self._store = JsonStore('store.json')
        
        if not 'not_notified' in self._store:
            self._store['not_notified'] = []

        if not 'notified' in self._store:
            self._store['notified'] = []

    def get_retocked(self) -> List[RestockedItem]:
        scrapers = [
            SupremeScraper(self._driver)
        ]

        for scraper in scrapers:
            scraped = scraper.get_restocked(self._get_all_items())

            all_items = self._get_all_items()
            new_items = [i for i in scraped if i not in all_items]
            
            self._add_to_not_notified(new_items)

        return self._as_items(self._store['not_notified'])

    def _get_all_items(self):
        return [RestockedItem(**i) for i in self._store['not_notified'] + self._store['notified']]

    def _add_to_not_notified(self, items):
        self._store['not_notified'] = self._store['not_notified'] + self._as_dicts(items)

    @staticmethod
    def _as_dicts(items):
        return [asdict(i) for i in items]

    @staticmethod
    def _as_items(dicts):
        return [RestockedItem(**i) for i in dicts]

    def set_notified(self, item):
        not_notified = self._as_items(self._store['not_notified'])
        notified = self._as_items(self._store['notified'])

        not_notified.remove(item)
        notified.append(item)

        self._store['not_notified'] = self._as_dicts(not_notified)
        self._store['notified'] = self._as_dicts(notified)
