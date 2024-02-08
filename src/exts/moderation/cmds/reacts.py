from interactions import *
from interactions.api.events import MessageCreate


class Reacts(Extension):

    @listen(MessageCreate)
    async def handle_msg(self, ctx: MessageCreate):
        content = ctx.message.content

        if 'sad' in content:
            await ctx.message.add_reaction('<:sob:>')


def setup(bot):
    Reacts(bot)
