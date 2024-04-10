from interactions import *
from interactions.api.events import MessageDelete, MessageUpdate

from src.exts.moderation.moderation_ext import ModerationExtension


class Snipe(Extension):
    def __init__(self, bot):
        self.last_message: Message = None
        self.stored_messages: list[Message] = []
        self.max_stored_messages: int = 3

    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='snipe',
                                                  sub_cmd_description='Retrieve the last deleted message')
    async def snipe(self, ctx: SlashContext):
        msg = None if len(self.stored_messages) <= 0 else self.stored_messages[0].content
        await ctx.send(f'Last Message: {msg}')

    @listen(MessageUpdate)
    async def on_message_update(self, edited_message: MessageUpdate):
        self.last_message = edited_message.before
        self.stored_messages.insert(0, self.last_message)
        if len(self.stored_messages) > self.max_stored_messages:
            self.stored_messages = self.stored_messages[:self.max_stored_messages]
        print(f'Updated message: {self.last_message.content}')

    @listen(MessageDelete)
    async def on_message_delete(self, deleted_message: MessageDelete):
        self.last_message = deleted_message.message
        self.stored_messages.insert(0, self.last_message)
        if len(self.stored_messages) > self.max_stored_messages:
            self.stored_messages = self.stored_messages[:self.max_stored_messages]
        print(f'Deleted message: {self.last_message.content}')


def setup(bot):
    Snipe(bot)
