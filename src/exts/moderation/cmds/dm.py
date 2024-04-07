from interactions import *
from src.exts.moderation.moderation_ext import ModerationExtension

class DM(Extension):

    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='dm',
                                                  sub_cmd_description='Actually banning someone')
    @slash_option(name='user',
                  description='The user to be banned',
                  opt_type=OptionType.USER,
                  required=True)
    @slash_option(name='msg',
                  description='Message to send',
                  opt_type=OptionType.STRING,
                  required=True)
    async def dm(self, ctx: SlashContext, user: User, msg: str):
        await user.send(msg)
        await ctx.send(f'Message sent!')

def setup(bot):
    DM(bot)