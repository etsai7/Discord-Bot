import interactions
import credentials

# intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
intents = interactions.Intents.AUTO_MOD | interactions.Intents.GUILD_MODERATION | interactions.Intents.GUILDS
client = interactions.Client(intents=intents, description="Testing Description", send_command_tracebacks=False)
item_suggestions = None


@interactions.listen()
async def on_ready():
    # We can use the client "me" attribute to get information about the bot.
    print(f"We're online! We've logged in as {client.user.username}.")

    # We're also able to use property methods to gather additional data.
    print(f"Our latency is {client.latency} ms.")


client.load_extension("exts.hypixel_ext")
client.load_extension("exts.test_ext")
client.load_extension("exts.buttons_ext")
client.load_extension("exts.moderation_ext")
client.start(credentials.discord_bot_token)
