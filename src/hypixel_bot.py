import interactions
import credentials
import sqlite3

# intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
intents = interactions.Intents.AUTO_MOD | interactions.Intents.GUILD_MODERATION | interactions.Intents.GUILDS | interactions.Intents.MESSAGE_CONTENT | interactions.Intents.MESSAGES
# intents = interactions.Intents.ALL
client = interactions.Client(intents=intents, description="Testing Description", send_command_tracebacks=False)
item_suggestions = None

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


def handle_db():
    create_table_query = '''CREATE TABLE If NOT EXISTS points (
                          User TEXT PRIMARY KEY,
                          Points INTEGER
                      )'''
    cursor.execute(create_table_query)
    client.db = cursor
    client.conn = connection


def load_extensions():
    client.load_extension("exts.hypixel_ext")
    client.load_extension("exts.buttons_ext")
    load_test_exts()
    load_moderation_exts()
    load_games_exts()
    load_points_exts()


def load_moderation_exts():
    client.load_extension("exts.moderation.moderation_ext")
    client.load_extension("exts.moderation.cmds.switch_role")
    client.load_extension("exts.moderation.cmds.ban")
    client.load_extension("exts.moderation.cmds.mute")
    client.load_extension("exts.moderation.cmds.poll")
    client.load_extension("exts.moderation.cmds.reacts")
    client.load_extension("exts.moderation.cmds.dm")
    client.load_extension("exts.moderation.cmds.snipe")


def load_points_exts():
    client.load_extension("exts.points.points_ext")
    client.load_extension("exts.points.points.points_cmds")


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

handle_db()
load_extensions()

client.start(credentials.discord_bot_token)
