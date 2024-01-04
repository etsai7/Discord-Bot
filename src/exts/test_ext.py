from interactions import Extension, slash_command, SlashContext, Embed, EmbedFooter, Timestamp, Color
import src.credentials as credentials


class TestExtension(Extension):
    @slash_command(name='testing',
                   scopes=[credentials.discord_guild_id],
                   sub_cmd_name='testext',
                   sub_cmd_description='Command to auto suggest a bunch of hypixel item choices')
    async def testExtension(self, ctx: SlashContext):
        await ctx.send("Hello Test Extension")

    @testExtension.subcommand(sub_cmd_name='testembed',
                              sub_cmd_description='Command to create an embed')
    async def testEmbed(self, ctx: SlashContext):
        embed = Embed(
            title="# **your title**",
            color=Color.from_rgb(201, 234, 252),
            description="your description",
            footer=EmbedFooter(text='This is a footer'),
            timestamp=Timestamp.now(),
            url='https://bongo.cat/')
        embed.set_thumbnail('https://i.pinimg.com/736x/52/fd/0c/52fd0ca64986b84c254726406cee5b6a.jpg')
        embed.add_field('key1', 'value1', inline=False)
        embed.add_field('key2', 'value2', inline=True)
        embed.add_field('key3', 'value3', inline=True)
        embed.add_field('Search', '[Google](https://www.google.com/)', inline=True)
        await ctx.send(embeds=embed)

    @testExtension.subcommand(sub_cmd_name='testhyperlink',
                              sub_cmd_description='Command to create a body of text with Hyperlink')
    async def testHyperLink(selfself, ctx: SlashContext):
        await ctx.send('Go to [Google](https://www.google.com/)')

# Bongo Cat