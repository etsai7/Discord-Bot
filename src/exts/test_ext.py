from interactions import Extension, slash_command, SlashContext
import src.credentials as credentials


class TestExtension(Extension):
    @slash_command(name='testext',
                   description='Command to auto suggest a bunch of hypixel item choices',
                   scopes=[credentials.discord_guild_id])
    async def testExtension(self, ctx: SlashContext):
        await ctx.send("Hello Test Extension")
