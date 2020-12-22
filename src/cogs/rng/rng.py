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

from ..errors import BadRepeatInput
from .die import Die


class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_roll(self, ctx, die_ob: Die, repeat: int = 1):
        rolls = [die_ob.roll() for i in range(repeat)]

        name = str(die_ob)

        message = f"Rolling {name}, {repeat} times"

        appendage = "\n".join(
            f'Individually: ({", ".join([str(i) for i in roll])}); Sum: ({sum(roll)})'
            for roll in rolls
        )

        await ctx.send(message + "\n" + appendage)

    @commands.command(usage="[amount]d[sides] [repeat=1]")
    async def roll(self, ctx, die: Die, repeat: int = 1):
        """Rolls a Die.

        Example usage: {prefix}roll 1d6 will roll a 6 sided die 1 time.
        """

        if repeat <= 0:
            raise BadRepeatInput()

        if not die:
            return

        return await self.send_roll(ctx, die, repeat)
