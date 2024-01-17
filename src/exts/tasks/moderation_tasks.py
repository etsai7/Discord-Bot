from interactions import *

class ModerationTasks(Extension):
    def __init__(self, bot, ctx: SlashContext):
        self.ctx = ctx

    async def unban(self):
        await self.ctx.guild.unban(user=self.ctx.user, reason='Did the time')