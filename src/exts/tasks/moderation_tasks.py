from interactions import *


class ModerationTasks(Extension):
    def __init__(self, bot, ctx: SlashContext, user: User):
        self.ctx = ctx
        self.user = user

    async def unban(self):

        await self.ctx.guild.unban(user=self.user, reason='Did the time')
        print('Unbanning Members')

        # --- This is not possible to re-invite/dm a person that is not in the Bot's server
        # await self.bot.fetch_user(self.user.id).send('https://discord.gg/CS2v46enp8')
        # usr = await self.bot.fetch_user(user_id=self.user.id)
        # print(f'Got the user: {usr}')
        # print(f'Original user: {self.user}')
        # await usr.send(content='https://discord.gg/CS2v46enp8')
        # await self.ctx.user.send(content='https://discord.gg/CS2v46enp8')
        # await usr.send('https://discord.gg/CS2v46enp8')
        # await self.ctx.channel.create_invite(max_uses=1, target_user=self.user, reason='Welcome back from exile')
