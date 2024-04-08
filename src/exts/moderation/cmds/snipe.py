from interactions import *
from interactions.api.events import MessageDelete

from src.exts.moderation.moderation_ext import ModerationExtension


class Snipe(Extension):
    def __init__(self, bot):
        self.deleted_message: MessageDelete = None

    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='snipe',
                                                  sub_cmd_description='Retrieve the last deleted message')
    async def snipe(self, ctx: SlashContext):
        await ctx.send(f'Last Message: {self.deleted_message.message.content}')

    @listen(MessageDelete)
    async def on_message_delete(self, deleted_message: MessageDelete):
        self.deleted_message = deleted_message
        print(f'Deleted message: {deleted_message.message.content}')


def setup(bot):
    Snipe(bot)
