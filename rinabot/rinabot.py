import logging

import asyncpg
from discord.ext import commands
import ruamel.yaml

class RinaBot(commands.Bot):
    def __init__(self, config):
        super().__init__(
            command_prefix=commands.when_mentioned, case_insensitive=True
        )

        self.config = config

        extensions = ['jishaku']

        for cog in extensions:
            self.load_extension(cog)

    @classmethod
    def with_config(cls):
        with open('config.yaml', encoding='utf-8') as f:
            data = ruamel.yaml.safe_load(f)
        return cls(data)

    def run(self):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('[%(asctime)s] (%(levelname)s) %(name)s: %(message)s', datefmt='%y %b %d %H:%M:%S')
        )
        logger.addHandler(handler)

        super().run(self.config['bot']['token'])

    async def start(self, *args, **kwargs):
        self.pool = await asyncpg.create_pool(**self.config['postgres'])

        await super().start(*args, **kwargs)
