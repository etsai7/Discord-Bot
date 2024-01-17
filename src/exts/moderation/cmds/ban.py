from interactions import *
from src.exts.moderation.moderation_ext import ModerationExtension
from datetime import datetime


class Ban(Extension):
    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='ban',
                                                  sub_cmd_description='Actually banning someone')
    @slash_option(name='user',
                  description='The user to be banned',
                  opt_type=OptionType.USER,
                  required=True)
    async def ban_user(self, ctx: SlashContext, user: Member):
        await user.edit(communication_disabled_until=Timestamp(datetime.now()))
        await ctx.guild.ban(user=user, reason='testing')
        await ctx.send('Banned!!')


def setup(bot):
    Ban(bot)
