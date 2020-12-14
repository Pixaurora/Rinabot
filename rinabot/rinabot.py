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
from discord import Intents
from discord.ext import commands

async def get_prefix(bot, message):
    default_prefix = [f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']
    if not message.guild:
        return default_prefix
    prefixes = await bot.pool.fetchval("""
    SELECT prefixes
        FROM guild_prefixes
        WHERE guild_id = $1
    """, message.guild.id)

    if prefixes == None:
        return default_prefix
    else:
        return default_prefix + prefixes

class RinaBot(commands.Bot):
    def __init__(self, config):

        intents = Intents.all()

        intents.typing = False
        intents.voice_states = False

        super().__init__(command_prefix=get_prefix, case_insensitive=True, intents=intents)

        self.config = config

        extensions = ["jishaku", "rinabot.cogs.prefix", "rinabot.cogs.errors", "rinabot.cogs.rng"]

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

    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        return await super().on_message(message)

    async def handle_guild(self, guild):
        entry = await self.pool.fetchrow("""
        SELECT *
            FROM guilds
            WHERE id = $1
        """, guild.id)

        if entry == None:
            await self.pool.execute("""
            INSERT INTO guilds (id, name, icon_hash)
                VALUES ($1, $2, $3)
            """, guild.id, guild.name, guild.icon)
        else:
            if entry['icon_hash'] != guild.icon:
                await self.pool.execute("""
                UPDATE guilds
                    SET icon_hash = $1
                    WHERE id = $2
                """, guild.icon, guild.id)
            if entry['name'] != guild.name:
                await self.pool.execute("""
                UPDATE guilds
                    SET name = $1
                    WHERE id = $2
                """, guild.name, guild.id)


    async def on_guild_available(self, guild):
        await self.handle_guild(guild)

    async def start(self, *args, **kwargs):
        self.pool = await asyncpg.create_pool(**self.config["postgres"])

        await super().start(*args, **kwargs)
