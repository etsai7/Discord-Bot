import interactions
import credentials

# intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
intents = interactions.Intents.AUTO_MOD | interactions.Intents.GUILD_MODERATION | interactions.Intents.GUILDS | interactions.Intents.MESSAGE_CONTENT | interactions.Intents.MESSAGES
client = interactions.Client(intents=intents, description="Testing Description", send_command_tracebacks=False)
item_suggestions = None


def load_extensions():
    client.load_extension("exts.hypixel_ext")
    client.load_extension("exts.buttons_ext")
    load_test_exts()
    load_moderation_exts()
    load_games_exts()


def load_moderation_exts():
    client.load_extension("exts.moderation.moderation_ext")
    client.load_extension("exts.moderation.cmds.switch_role")
    client.load_extension("exts.moderation.cmds.ban")
    client.load_extension("exts.moderation.cmds.mute")
    client.load_extension("exts.moderation.cmds.poll")
    client.load_extension("exts.moderation.cmds.reacts")


def load_games_exts():
    client.load_extension("exts.games.games_ext")
    client.load_extension("exts.games.rps.rock_paper_scissors")


def load_test_exts():
    client.load_extension("exts.testing.test_ext")
    client.load_extension("exts.testing.countdown")


@interactions.listen()
async def on_ready():
    # We can use the client "me" attribute to get information about the bot.
    print(f"We're online! We've logged in as {client.user.username}.")

    # We're also able to use property methods to gather additional data.
    print(f"Our latency is {client.latency} ms.")


load_extensions()

client.start(credentials.discord_bot_token)
