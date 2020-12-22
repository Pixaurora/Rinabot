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

from ...config import GUILD_ID, JOIN_CHANNEL_ID, JOIN_EMOJI, LEAVE_EMOJI


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_guild(GUILD_ID).get_channel(JOIN_CHANNEL_ID)

        bots = sum(member.bot for member in guild.members)
        humans = len(guild.members) - bots

        await channel.send(
            f"{JOIN_EMOJI} Joined {guild.name} ({guild.id}) - {humans} humans - {bots} bots"
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_guild(GUILD_ID).get_channel(JOIN_CHANNEL_ID)

        await channel.send(f"{LEAVE_EMOJI} Left {guild.name} ({guild.id})")
