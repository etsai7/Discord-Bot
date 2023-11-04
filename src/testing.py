import time

import interactions
import credentials
import random
from src.utils import Hypixel_items

intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
client = interactions.Client(intents=intents, description="Testing Description")
item_suggestions = None

# Slash Commands Site: https://interactions-py.github.io/interactions.py/Guides/03%20Creating%20Commands/#__tabbed_1_1

@interactions.listen()
async def on_ready():
    # We can use the client "me" attribute to get information about the bot.
    print(f"We're online! We've logged in as {client.user.username}.")

    # We're also able to use property methods to gather additional data.
    print(f"Our latency is {(client.latency)} ms.")
    # await runLoop()

    Hypixel_items.refresh_mappings()
    global item_suggestions
    item_suggestions = Hypixel_items.read_mappings_from_json()

    # for i in range (0,10):
    #     print(item_suggestions[i])


# async def runLoop():
#     while True:
#         print("Sleeping for 5")
#         time.sleep(5)

# We can either pass in the event name or make the function name be the event name.
@interactions.listen("on_message_create")
async def name_this_however_you_want(message_create: interactions.events.MessageCreate):
    # Whenever we specify any other event type that isn't "READY," the function underneath
    # the decorator will most likely have an argument required. This argument is the data
    # that is being supplied back to us developers, which we call a data model.

    # In this example, we're listening to messages being created. This means we can expect
    # a "message_create" argument to be passed to the function, which will contain the
    # data model for the message

    # We can use the data model to access the data we need.
    # Keep in mind that you can only access the message content if your bot has the MESSAGE_CONTENT intent.
    # You can find more information on this in the migration section of the quickstart guide.
    message: interactions.Message = message_create.message
    print(f"We've received a message from {message.author.username}. The message is: {message.content}.")


# Now, let's create a command.
# A command is a function that is called when a user types out a command.
# The command is called with a context object, which contains information about the user, the channel, and the guild.
# Context is what we call the described information given from an interaction response, what comes from a command.
# The context object in this case is a class for commands, but can also be one for components if used that way.
@interactions.slash_command(name="hello-world",
                            description='A command that says "hello world!"',
                            scopes=[credentials.discord_guild_id])
async def hello_world(ctx: interactions.SlashContext):
    # "ctx" is an abbreviation of the context object.
    # You don't need to type hint this, but it's recommended to do so.

    # Now, let's send back a response.
    # The interaction response should be the LAST thing you do when a command is ran.
    await ctx.send("I'm alive!!!!")

    # However, any code you put after a response will still execute unless you prevent it from doing so.
    print("we ran.")


@interactions.slash_command(name='hey-partybot', description='A command that PartyBot will reply with snarky responses',
                            scopes=[credentials.discord_guild_id])
async def hey_partybot(ctx: interactions.SlashContext):
    responses = ["What?", "Leave me alone!", "Stop bothering me", "No", "Whyyyy??"]
    await ctx.send(random.choice(responses))

# Sub Commands
@interactions.slash_command(
    name="base",
    description="My command base",
    scopes=[credentials.discord_guild_id],
    group_name="group",
    group_description="My command group",
    sub_cmd_name="command",
    sub_cmd_description="My command",
)
async def my_command_function(ctx: interactions.SlashContext):
    await ctx.send("Hello World")


@my_command_function.subcommand(
    group_name="group",
    group_description="My command group",
    sub_cmd_name="sub",
    sub_cmd_description="My subcommand",
)
async def my_second_command_function(ctx: interactions.SlashContext):
    await ctx.send("Hello World 2")


# Adding options
@interactions.slash_command(name="option_command",
                            description="A command to test with additional options",
                            scopes=[credentials.discord_guild_id])
@interactions.slash_option(
    name="integer_option",
    description="Integer Option",
    required=True,
    opt_type=interactions.OptionType.INTEGER
)
async def my_command_function(ctx: interactions.SlashContext, integer_option: int):
    await ctx.send(f"You input {integer_option}")


# Adding multiple options
@interactions.slash_command(name='add', description='A command will respond with added values',
                            scopes=[credentials.discord_guild_id])
@interactions.slash_option(
    name="one",
    description="Integer Option",
    required=True,
    opt_type=interactions.OptionType.INTEGER
)
@interactions.slash_option(
    name="two",
    description="Integer Option",
    required=True,
    opt_type=interactions.OptionType.INTEGER
)
async def add(ctx: interactions.SlashContext, one: int, two: int):
    await ctx.send(f'{one} + {two} = {one + two}')


@interactions.slash_command(name='fruit_choices', description='Making the user select pre-populated choices',
                            scopes=[credentials.discord_guild_id])
@interactions.slash_option(
    name='fruit',
    description='Pick a fruit',
    required=True,
    opt_type=interactions.OptionType.STRING,
    choices=[
            interactions.SlashCommandChoice(name="Banana", value="Banana"),
            interactions.SlashCommandChoice(name="Apple", value="Apple"),
            interactions.SlashCommandChoice(name="Passion Fruit", value="Passion Fruit"),
        ]
)
async def fruit_choices(ctx: interactions.SlashContext, fruit: str):
    fruit_dict = {
        'Banana' : 'Na na na na Banana',
        'Apple'  : 'What a classic',
        'Passion Fruit' : 'So much Passion or something'
    }
    await ctx.send(f'You picked {fruit}, {fruit_dict[fruit]}')
@interactions.slash_command(name='at_user', description='Command to tag user',
                            scopes=[credentials.discord_guild_id])
@interactions.slash_option(
    name="user",
    description="User",
    required=True,
    opt_type=interactions.OptionType.USER
)
async def at_user(ctx: interactions.SlashContext, user: interactions.OptionType.USER):
    print(user)
    await ctx.send(f'Hey @{user.mention}')

@interactions.slash_command(name="timeout_test", description="Testing Discord timing out",
                            scopes=[credentials.discord_guild_id])
async def timeout_test(ctx: interactions.SlashContext):

    await ctx.send("Going to sleep for 4 seconds")
    time.sleep(4)

    await ctx.send("Sending response after sleeping for 4 seconds")

@interactions.slash_command(name='many_many_many_choices', description='Command to auto suggest a bunch of choices',
                            scopes=[credentials.discord_guild_id])
@interactions.slash_option(
    name='item',
    description="Item we want to autosuggest",
    required=True,
    opt_type=interactions.OptionType.STRING,
    autocomplete=True
)
async def many_many_many_choices(ctx: interactions.SlashContext, item: interactions.OptionType.STRING):
    await ctx.send(f"You selected {item}")

@many_many_many_choices.autocomplete("item")
async def autocomplete(ctx: interactions.AutocompleteContext):
    item = ctx.input_text

    await ctx.send(
        choices=
        [
            {
                "name": f"{item}a",
                "value": f"{item}a",
            },
            {
                "name": f"{item}b",
                "value": f"{item}b",
            },
            {
                "name": f"{item}c",
                "value": f"{item}c",
            },
            {
                "name": f"{item}d",
                "value": f"{item}d",
            },
            {
                "name": f"{item}e",
                "value": f"{item}e",
            },
            {
                "name": f"{item}f",
                "value": f"{item}f",
            },
            {
                "name": f"God Potion",
                "value": f"God Potion"
            }
        ]
    )

@interactions.slash_command(name='hypixel_item_choices', description='Command to auto suggest a bunch of hypixel item choices',
                            scopes=[credentials.discord_guild_id])
@interactions.slash_option(
    name='item',
    description="Item we want to autosuggest",
    required=True,
    opt_type=interactions.OptionType.STRING,
    autocomplete=True
)
async def hypixel_item_choices(ctx: interactions.SlashContext, item: interactions.OptionType.STRING):
    print(f'Command Message - ID: {ctx.message_id} -> {ctx.message}')
    message_sent = await ctx.send(f"You selected {item}")
    print(f'Message Sent: {message_sent}')


@hypixel_item_choices.autocomplete("item")
async def autocomplete(ctx: interactions.AutocompleteContext):
    item = ctx.input_text
    # interactions.Message.edit()

    filtered_choices = [entry for entry in item_suggestions if entry.get("name", "").startswith(item)][:25]
    print(f'AutoComplete Message - ID: {ctx.message_id} -> {ctx.message}')

    await ctx.send(
        choices=filtered_choices
    )

client.start(credentials.discord_bot_token)