from interactions import *
from interactions.api.events import MessageDelete, MessageUpdate, Component

from src.exts.moderation.moderation_ext import ModerationExtension
from PIL import Image, ImageDraw, ImageFont


class Snipe(Extension):
    def __init__(self, bot):
        self.choices = ['snipe_back', 'snipe_forward']
        self.last_message: Message = None
        self.stored_messages: list[Message] = []
        self.max_stored_messages: int = 3

    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='snipe',
                                                  sub_cmd_description='Retrieve the last deleted message')
    @slash_option(name='last',
                  description='Last x message to snipe',
                  opt_type=OptionType.INTEGER,
                  required=False)
    async def snipe(self, ctx: SlashContext, last: int = 1):
        msg = None if len(self.stored_messages) < last else self.stored_messages[last - 1].content
        embed = Embed(
            title="**Sniped**",
            color=Color.from_rgb(201, 234, 252),
            description=f'{msg}',
            footer=EmbedFooter(text='This is a footer'),
            timestamp=Timestamp.now(),
            url='https://bongo.cat/')
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @listen(MessageUpdate)
    async def on_message_update(self, edited_message: MessageUpdate):
        if not edited_message.before.content and not edited_message.after.content:
            print('before and after update not needed because empty on both sides')
            return
        print(f'Before: {edited_message.before.content} after: {edited_message.after.content}')
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

    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='snipe_scroll',
                                                  sub_cmd_description='Scroll through modified messages')
    async def snipe_scroll(self, ctx: SlashContext):
        msg = None if len(self.stored_messages) <= 0 else self.stored_messages[0].content
        embed = Embed(
            title="**Sniped**",
            color=Color.from_rgb(201, 234, 252),
            description=f'{msg}',
            timestamp=Timestamp.now())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, components=self.build_buttons())

    def build_buttons(self) -> list[Button]:
        return [Button(
            style=ButtonStyle.SECONDARY,
            emoji='◀',
            custom_id=f'snipe_back'
        ), Button(
            style=ButtonStyle.SECONDARY,
            emoji='▶',
            custom_id=f'snipe_forward',
        )]

    @listen(Component)
    async def my_callback(self, event: Component):
        ctx = event.ctx
        user_name = ctx.user.display_name
        direction = ctx.custom_id

        # Prevent overlaps with other buttons from other commands. Skip if id isn't valid
        if direction not in self.choices:
            return

        msg_obj = ctx.message
        msg_obj_embed = msg_obj.embeds[0]
        msg = msg_obj_embed.description
        msg_index = self.find_message(msg)
        for n in self.stored_messages:
            print(f'\t{n.content}')

        self.find_user(user_name, ctx)

        if direction == 'snipe_back':
            new_msg_index = max(0, msg_index - 1)
            msg_obj_embed.description = self.stored_messages[new_msg_index].content
            print(f'Moving back to index {new_msg_index} with message {msg_obj_embed.description}')
        else:
            new_msg_index = min(len(self.stored_messages)-1, msg_index + 1)
            msg_obj_embed.description = self.stored_messages[new_msg_index].content
            print(f'Moving forward to index {new_msg_index} with message {msg_obj_embed.description}')

        await msg_obj.edit(embed=msg_obj_embed)
        await ctx.defer(edit_origin=True)

    def find_message(self, message: str):
        for i in range(len(self.stored_messages)):
            print(f'\t\tComparing: passed message: {message} vs array {self.stored_messages[i].content}')
            if message == self.stored_messages[i].content:
                return i
        return -1

    def find_user(self, user: str, ctx: ComponentContext):
        for users in ctx.channel.members:
            print(f'Given: {user}, find User: {users.display_name}')

    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='quote_to_img',
                                                  sub_cmd_description='Converte a Quote to an Image')
    @slash_option(name='quote',
                  description='Quote',
                  opt_type=OptionType.STRING,
                  required=True)
    async def convert_quote_to_img(self, ctx: SlashContext, quote: str) -> None:
        self.generate_quote_img(quote)
        file = File(file=r"./exts/moderation/outputs/quote.jpg", file_name="quote.jpg")
        embed = Embed(title='Quote to Image', description="Quote Embed")
        embed.set_image('attachment://exts/moderation/outputs/quote.jpg')
        await ctx.send(files=file)

    def generate_quote_img(self, quote: str):
        # Define image properties
        width, height = 300, 200
        background_color = ( 204, 213, 174)  # White background color
        text_color = (212, 163, 115)  # Black text color
        text = quote

        # Create a new image with the specified background color
        image = Image.new("RGB", (width, height), background_color)

        # Initialize the drawing context
        draw = ImageDraw.Draw(image)

        # Define a font (change the path to a font file on your system)
        font = ImageFont.truetype("arial.ttf", 30)

        # Calculate text size and position

        text_width = draw.textlength(text, font=font)
        text_height = font.size
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw the text on the image
        draw.text((x, y), text, fill=text_color, font=font)

        image.show()
        # Save the image as JPEG or PNG
        image.save("./exts/moderation/outputs/quote.jpg")  # Save as JPEG
        # image.save("output.png")  # Save as PNG


def setup(bot):
    Snipe(bot)
