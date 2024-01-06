from interactions import Extension, slash_command, SlashContext, Embed, EmbedFooter, Timestamp, Color
import src.credentials as credentials


class TestExtension(Extension):
    @slash_command(name='testing',
                   scopes=[credentials.discord_guild_id],
                   sub_cmd_name='test_info',
                   sub_cmd_description='Command to auto suggest a bunch of hypixel item choices')
    async def testExtension(self, ctx: SlashContext):
        cmds = ('`test_info` - List of all the functions under the testing group\n`test_embed` - Testing default embed '
                'and layouts\n`test_hyperlink` - Hyperlinking a msg, using markdown format\n`bongocat` - Bongo Cat '
                'embed')
        await ctx.send(cmds)

    @testExtension.subcommand(sub_cmd_name='test_embed',
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

    @testExtension.subcommand(sub_cmd_name='test_hyperlink',
                              sub_cmd_description='Command to create a body of text with Hyperlink')
    async def testHyperLink(self, ctx: SlashContext):
        await ctx.send('Go to [Google](https://www.google.com/)')

    # Bongo Cat
    @testExtension.subcommand(sub_cmd_name='bongocat',
                              sub_cmd_description='Command for a Bongo Cat Embed')
    async def testBongoCatEmbed(self, ctx: SlashContext):
        embed = Embed(
            title='🥁 Bongo Cat',
            color=Color.from_rgb(27, 193, 87),
            # description="Bing Bong Bongo Cat at your Service",
            timestamp=Timestamp.now(),
            url='https://bongo.cat/'
        )
        # embed.set_thumbnail('https://i0.wp.com/boingboing.net/wp-content/uploads/2020/10/bongo-cat.jpg?fit=1380%2C903'
        #                     '&ssl=1')
        embed.set_thumbnail('https://media2.giphy.com/media/sthmCnCpfr8M8jtTQy/giphy.gif')
        embed.add_field('*Bing Bong*', 'Bongo Cat at your service')
        await ctx.send(embeds=embed)
