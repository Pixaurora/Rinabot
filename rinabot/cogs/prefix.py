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


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_pretty_prefixes(self, message):
        prefixes = [
            clean_prefix(self.bot, prefix)
            for prefix in await self.bot.command_prefix(self.bot, message)
        ]
        return [
            f"`{i.lstrip().rstrip()}`"
            for n, i in enumerate(prefixes)
            if i not in prefixes[:n]
        ]

    @commands.group()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand:
            return

        prefixes = await self.get_pretty_prefixes(ctx.message)

        await ctx.send(
            f'Prefix{["",  "es"][len(prefixes) > 1]}: {",".join(prefixes)}'
            + [
                "",
                f"\n```Prefix Subcommands:\n{clean_prefix(self.bot, ctx.prefix)}prefix add [prefix]\n{clean_prefix(self.bot, ctx.prefix)}prefix remove [prefix]```",
            ][ctx.author.guild_permissions.administrator]
        )

    @prefix.command()
    @commands.has_guild_permissions(administrator=True)
    async def add(self, ctx, *, prefix: str):
        if clean_prefix(self.bot, prefix) in await self.get_pretty_prefixes(
            ctx.message
        ):
            await ctx.send("This prefix has already been added!")
        else:
            prefixes = await self.bot.pool.fetchval(
                """
            SELECT prefixes
                FROM guild_prefixes
                WHERE guild_id = $1
            """,
                ctx.guild.id,
            )
            if prefixes == None:
                await self.bot.pool.execute(
                    """
                INSERT INTO guild_prefixes (guild_id, prefixes)
                    VALUES ($1, $2)
                """,
                    ctx.guild.id,
                    [prefix],
                )
            else:
                prefixes.append(prefix)
                await self.bot.pool.execute(
                    """
                UPDATE guild_prefixes
                    SET prefixes = $1
                    WHERE guild_id = $2
                """,
                    prefixes,
                    ctx.guild.id,
                )
            await ctx.send(
                f"Done! Added `{clean_prefix(self.bot, prefix)}` to this server's prefix list!"
            )

    @prefix.command()
    @commands.has_guild_permissions(administrator=True)
    async def remove(self, ctx, *, prefix: str):
        prefixes = await self.bot.pool.fetchval(
            """
        SELECT prefixes
            FROM guild_prefixes
            WHERE guild_id = $1
        """,
            ctx.guild.id,
        )

        if prefixes == None:
            await ctx.send("This guild has no custom prefixes!")
        elif clean_prefix(self.bot, prefix) == clean_prefix(
            self.bot, self.bot.user.mention
        ):
            await ctx.send(f"You can't remove mentioning me as a prefix!")
        elif not prefix in prefixes:
            await ctx.send(
                f"This guild doesn't have the prefix `{clean_prefix(self,prefix)}` in the list!"
            )
        else:
            prefixes.remove(prefix)
            await self.bot.pool.execute(
                """
            UPDATE guild_prefixes
                SET prefixes = $1
                WHERE guild_id = $2
            """,
                prefixes,
                ctx.guild.id,
            )
            await ctx.send(
                f"The prefix `{clean_prefix(self.bot, prefix)}` has been successfully removed!"
            )


def setup(bot):
    bot.add_cog(Prefix(bot))
