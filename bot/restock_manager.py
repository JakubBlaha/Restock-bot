from typing import List
from dataclasses import asdict

from jsonstore import JsonStore

from .scraper import Scraper, SupremeScraper
from .item import RestockedItem


class RestockManager:
    def __init__(self):
        self._driver = Scraper.get_reusable_driver()
        self._store = JsonStore('restocked.json')
        
        if not 'restocked' in self._store:
            self._store['restocked'] = []

        if not 'notified' in self._store:
            self._store['notified'] = []

    def get_retocked(self) -> List[RestockedItem]:
        scrapers = [
            SupremeScraper(self._driver)
        ]

        for scraper in scrapers:
            restocked = scraper.get_restocked()
            self._save_restocked(restocked)

        return self._get_not_notified()

    def _save_restocked(self, restocked):
        restocked = [asdict(i) for i in restocked]

        restock_list = self._store['restocked']
        restock_list.extend(restocked)
        self._store['restocked'] = restock_list

    def set_notified(self, item):
        notified = self._store['notified']
        notified.append(item.id)
        self._store['notified'] = notified

    def was_notified(self, id):
        return id in self._store['notified']

    def _get_not_notified(self):
        return [
            RestockedItem(**i) for i in self._store['restocked'] if i['id'] not in self._store['notified']
        ]