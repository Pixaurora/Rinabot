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

from discord.ext import commands

from .utils import clean_prefix


class Context(commands.Context):
    async def send(self, content=None, **kwargs):
        content = str(content) if content is not None else None

        if content is not None and len(content) > 2000:
            async with self.bot.session.post(
                "https://starb.in/documents", data=content
            ) as response:
                url = (await response.json())["url"]

                return await super().send(
                    f"The message was too big! View it here: {url}", **kwargs
                )

        return await super().send(content, **kwargs)

    @property
    def pretty_prefix(self):
        return clean_prefix(self.bot, self.prefix)
