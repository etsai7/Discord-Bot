from interactions import *
import src.credentials as credentials


class Games(Extension):
    @slash_command(name='games',
                   scopes=[credentials.discord_guild_id],
                   sub_cmd_name='info',
                   sub_cmd_description='Info on available games')
    async def game_info(self, ctx: SlashContext):
        embed = Embed(
            title="**🎮 Available Game Commands**",
            color=Color.from_rgb(201, 234, 252),
            footer=EmbedFooter(text='- PartyBot™'),
            timestamp=Timestamp.now())
        embed.add_field('`rps`', 'Rock Paper Scissor with the bot', inline=False)

        information = '''
        1. `rps` - Rock Paper Scissor with the bot
        '''
        await ctx.send(embeds=embed)
