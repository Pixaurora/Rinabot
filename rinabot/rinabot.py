"""
Rina Bot: Discord Bot for Something Probably
Copyright (C) 2020 Rina

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging

import asyncpg
import ruamel.yaml
from discord.ext import commands


class RinaBot(commands.Bot):
    def __init__(self, config):
        super().__init__(command_prefix=commands.when_mentioned, case_insensitive=True)

        self.config = config

        extensions = ["jishaku", "rinabot.cogs.prefix", "rinabot.cogs.errors"]

        for cog in extensions:
            self.load_extension(cog)

    @classmethod
    def with_config(cls):
        with open("config.yaml", encoding="utf-8") as f:
            data = ruamel.yaml.safe_load(f)
        return cls(data)

    def run(self):
        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] (%(levelname)s) %(name)s: %(message)s",
                datefmt="%y %b %d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

        super().run(self.config["bot"]["token"])

    async def start(self, *args, **kwargs):
        self.pool = await asyncpg.create_pool(**self.config["postgres"])

        await super().start(*args, **kwargs)
