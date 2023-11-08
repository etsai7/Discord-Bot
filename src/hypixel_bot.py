import time
import interactions
import credentials
from src.utils import Hypixel_items
from src.utils import Auction_House

intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
client = interactions.Client(intents=intents, description="Testing Description")
item_suggestions = None

@interactions.listen()
async def on_ready():
    # We can use the client "me" attribute to get information about the bot.
    print(f"We're online! We've logged in as {client.user.username}.")

    # We're also able to use property methods to gather additional data.
    print(f"Our latency is {(client.latency)} ms.")

    Hypixel_items.refresh_mappings()
    global item_suggestions
    item_suggestions = Hypixel_items.read_mappings_from_json()

@interactions.slash_command(name='hypixel_item_choices', description='Command to auto suggest a bunch of hypixel item choices',
                            scopes=[credentials.discord_guild_id])
@interactions.slash_option(
    name='item',
    description="Item we want to autosuggest",
    required=True,
    opt_type=interactions.OptionType.STRING,
    autocomplete=True
)
@interactions.slash_option(
    name='bin',
    description="Item we want to auto suggest",
    required=True,
    opt_type=interactions.OptionType.BOOLEAN,
    choices=[
        interactions.SlashCommandChoice(name="True", value=True),
        interactions.SlashCommandChoice(name="False", value=False)
    ]
)
@interactions.slash_option(
    name='limit',
    description="Item we want to auto suggest",
    required=False,
    opt_type=interactions.OptionType.INTEGER
)
async def hypixel_item_choices(ctx: interactions.SlashContext, item: interactions.OptionType.STRING, bin: interactions.OptionType.BOOLEAN = True, limit: interactions.OptionType.INTEGER = 1):
    print(f'Command Message - ID: {ctx.message_id} -> {ctx.message}')
    message_sent = await ctx.send(f"You selected {item} with a limit of {limit} entries, please hold while we retrieve your data")
    await ctx.edit(message_sent, content=Auction_House.handle_auction_data_retrieval(item, bin, limit))


@hypixel_item_choices.autocomplete("item")
async def autocomplete(ctx: interactions.AutocompleteContext):
    item = ctx.input_text

    filtered_choices = [entry for entry in item_suggestions if entry.get("name", "").startswith(item)][:25]
    # print(f'AutoComplete Message - ID: {ctx.message_id} -> {ctx.message}')

    await ctx.send(
        choices=filtered_choices
    )



client.start(credentials.discord_bot_token)