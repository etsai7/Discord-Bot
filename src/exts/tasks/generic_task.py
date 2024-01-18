from interactions import Extension, SlashContext, Client


class GenericTask(Extension):

    def __init__(self, bot: Client, ctx: SlashContext = None):
        self.ctx = ctx

    async def send_msg_delayed(self):
        print('Message was delayed')
        await self.ctx.send('Message Was Successfully delayed')
