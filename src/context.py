import aiohttp
from discord.ext import commands

class Context(commands.Context):
    async def send(self, content=None, **kwargs):
        content = str(content) if content is not None else None

        if content is not None and len(content) > 2000:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://starb.in/documents', data=content) as response:
                    url = (await response.json())['url']

                    return await super().send(f'The message was too big! View it here: {url}')

        await super().send(content, **kwargs)
