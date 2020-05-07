import sys
import logging

from discord.ext.commands import Bot

from .config import conf


class DiscordBot(Bot):
    async def on_ready(self):
        logging.info('Logged in as {0.user}'.format(self))


logging.basicConfig(handlers=[logging.FileHandler(
    'log.log'), logging.StreamHandler(sys.stdout)],
    level=logging.INFO)


if __name__ == "__main__":
    DiscordBot('!').run(conf['token'])
