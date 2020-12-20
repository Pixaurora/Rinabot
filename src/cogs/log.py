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

from .errors.utils import clean_prefix


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.join_emoji = self.bot.config["bot"]["join_emoji"]
        self.leave_emoji = self.bot.config["bot"]["leave_emoji"]

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_guild(self.bot.config["bot"]["guild_id"]).get_channel(
            self.bot.config["bot"]["join_channel_id"]
        )

        bots = sum(member.bot for member in guild.members)

        humans = len(guild.members) - bots

        await channel.send(
            f"{self.join_emoji} Joined {guild.name} ({guild.id}) - {humans} humans - {bots} bots"
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_guild(self.bot.config["bot"]["guild_id"]).get_channel(
            self.bot.config["bot"]["join_channel_id"]
        )

        await channel.send(f"{self.leave_emoji} Left {guild.name} ({guild.id})")


def setup(bot):
    bot.add_cog(Log(bot))
