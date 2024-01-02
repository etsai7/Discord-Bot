from interactions import Extension, slash_command, SlashContext, Embed, EmbedFooter, Timestamp, Color
import src.credentials as credentials


class TestExtension(Extension):
    @slash_command(name='testext',
                   description='Command to auto suggest a bunch of hypixel item choices',
                   scopes=[credentials.discord_guild_id])
    async def testExtension(self, ctx: SlashContext):
        await ctx.send("Hello Test Extension")

    @slash_command(name='test_embed', description='Command to create an embed',
                                scopes=[credentials.discord_guild_id])
    async def testEmbed(ctx: SlashContext):
        embed = Embed(
            title="your title",
            color=Color.from_rgb(201, 234, 252),
            description="your description",
            footer=EmbedFooter(text='This is a footer'),
            timestamp=Timestamp.now())
        embed.set_thumbnail('https://i.pinimg.com/736x/52/fd/0c/52fd0ca64986b84c254726406cee5b6a.jpg')
        await ctx.send(embeds=embed)