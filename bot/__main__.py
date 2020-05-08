import logging
import sys
import asyncio
import random
from typing import List

from discord import Embed, TextChannel
from discord.ext.commands import Bot
from discord.ext.tasks import loop

from .config import conf
from .item import RestockedItem
from .restock_manager import RestockManager


class DiscordBot(Bot):
    _notif_channel: TextChannel

    async def on_ready(self):
        logging.info('Logged in as {0.user}'.format(self))

        self._restock_manager = RestockManager()
        self._notif_channel = self.get_channel(int(conf['notification_channel_id']))

        self.work.start()

    @loop(seconds=10)
    async def work(self):
        await asyncio.sleep(random.random() * 5)

        restocked = self._restock_manager.get_retocked()

        await self._send_restocks(restocked)

    async def _send_restocks(self, restocked: List[RestockedItem]):
        for restock in restocked:
            await self._send_restock(restock)
            self._restock_manager.set_notified(restock)

    async def _send_restock(self, item: RestockedItem):
        e = Embed(title=item.title, description=item.description, url=item.url)
        e.set_thumbnail(url=item.image)
        e.add_field(name='Price', value=item.price)

        await self._notif_channel.send(embed=e)


logging.basicConfig(handlers=[logging.FileHandler(
    'log.log'), logging.StreamHandler(sys.stdout)],
    level=logging.INFO)


if __name__ == "__main__":
    DiscordBot('!').run(conf['token'])
