from discord.ext import commands

import re
import textwrap

import random


class Die:
    __slots__ = ("amount", "faces", "name")

    def __init__(self, amount: int, faces: int):
        if amount <= 0 or faces <= 0:
            raise ValueError("Incorrect format.")

        self.amount = amount
        self.faces = faces

    def __call__(self):
        return [random.randint(1, self.faces) for i in range(self.amount)]

    def __str__(self):
        return f"{self.amount}d{self.faces}"

    @classmethod
    def from_string(cls, string):
        try:
            return cls(*[int(i) for i in re.compile(r"^(\d+)d(\d+)$").findall(string)[0]])
        except IndexError:
            raise KeyError("Incorrect format.")


class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_roll(self, ctx, dice_ob: Die, repeat: int = 1):
        rolls = [dice_ob() for i in range(repeat)]

        name = str(dice_ob)

        message = f"Rolling __{name}__ {repeat} times"

        appendage = "\n".join(
            [
                "Individually: ({}); Sum: ({})".format(
                    ", ".join([str(i) for i in roll]), sum(roll)
                )
                for roll in rolls
            ]
        )

        await ctx.send(message + "\n" + appendage)

    async def get_dice(self, ctx, name):
        try:
            return Die.from_string(name)
        except KeyError:
            await ctx.send("Incorrect format. Correct format is XdX.")
        except ValueError:
            await ctx.send("Incorrect format. Make sure all numbers are above 0.")

    async def bad_repeat(self, ctx, repeat):
        if repeat == 0:
            return await ctx.send("You can't roll 0 times.")
        elif repeat <= 0:
            return await ctx.send("You can't doll negative times.")

    @commands.group(name="roll", brief="Rolls a dice", invoke_without_command=True)
    async def roll(self, ctx, dice_name: str = None, repeat: int = 1):
        """Rolls a Dice

        Use the command to see a guide.
        """

        if dice_name:
            if await self.bad_repeat(ctx, repeat):
                return
            dice = await self.get_dice(ctx, dice_name)

            if not dice:
                return

            return await self.send_roll(ctx, dice, repeat)

        else:

            await ctx.send(
                textwrap.dedent(
                    """
                    __**Dice Guide**__
                    **Basic Info**
                    > *Syntax:* >roll (dice name) (amount of rolls)
                    > An amount of rolls is optional and will default to 1.
                    > In addition to the premade die avaliable theres also custom die!
                    > Enjoy!
                    **Premade Dice** 
                    > ** **
                    **Custom die**
                    > To make custom die, simply use this format: (amount)d(sides)
                    > Amount just means how many die to use, and sides is the max number you can roll
                    """
                )
            )



def setup(client):
    client.add_cog(RNG(client))
