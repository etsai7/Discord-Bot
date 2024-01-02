from interactions import Extension, slash_command, SlashContext, OptionType, SlashCommandChoice, slash_option, \
    AutocompleteContext
import src.credentials as credentials
import src.utils.Auction_House as Auction_House
import src.utils.Hypixel_items as Hypixel_items


class HypixelExtension(Extension):
    def __init__(self, bot):
        Hypixel_items.refresh_mappings()
        self.item_suggestions = Hypixel_items.read_mappings_from_json()

    @slash_command(name='hypixel_item_choices',
                   description='Command to auto suggest a bunch of hypixel item choices',
                   scopes=[credentials.discord_guild_id])
    @slash_option(
        name='item',
        description="Item we want to autosuggest",
        required=True,
        opt_type=OptionType.STRING,
        autocomplete=True
    )
    @slash_option(
        name='bin',
        description="Item we want to auto suggest",
        required=True,
        opt_type=OptionType.BOOLEAN,
        choices=[
            SlashCommandChoice(name="True", value=True),
            SlashCommandChoice(name="False", value=False)
        ]
    )
    @slash_option(
        name='limit',
        description="Item we want to auto suggest",
        required=False,
        opt_type=OptionType.INTEGER
    )
    async def hypixel_item_choices(self, ctx: SlashContext, item: OptionType.STRING,
                                   bin: OptionType.BOOLEAN = True,
                                   limit: OptionType.INTEGER = 1):
        print(f'Command Message - ID: {ctx.message_id} -> {ctx.message}')
        message_sent = await ctx.send(
            f"You selected {item} with a limit of {limit} entries, please hold while we retrieve your data")

        await ctx.edit(message_sent, content=Auction_House.handle_auction_data_retrieval(item, bin, limit))

    @hypixel_item_choices.autocomplete("item")
    async def autocomplete(self, ctx: AutocompleteContext):
        item = ctx.input_text
        filtered_choices = [entry for entry in self.item_suggestions if entry.get("name", "").startswith(item)][:25]
        # print(f'AutoComplete Message - ID: {ctx.message_id} -> {ctx.message}')

        await ctx.send(
            choices=filtered_choices
        )
